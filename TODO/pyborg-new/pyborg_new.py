#
# PyBorg: The python AI bot.
#
# Copyright (c) 2000, 2006, 2013-2021 Tom Morton, Sebastien Dailly, Jack Laxson
#
#
# This bot was inspired by the PerlBorg, by Eric Bock.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# Tom Morton <tom@moretom.net>
# Seb Dailly <seb.dailly@gmail.com>
# Jack Laxson <jackjrabbit+pyborg@gmail.com>

import logging
import re
import sys
import time
from random import randint
from typing import List, Optional, Tuple
import mmh3
import nltk
import spacy
from loguru import logger
from models_sql import Line, Word

import random



def filter_messages(message_list: List[str], bot) -> List[str]:
    """
    Filter a message body so it is suitable for learning from and
    replying to. This involves removing confusing characters,
    padding ? and ! with ". " so they also terminate lines
    and converting to lower case.
    """
    messages = []
    url_pattern = re.compile(r'https?://|www\.')
    for message in message_list:
        if not message[0].isalnum():
            continue

        # Verificar se a mensagem contém um link.
        if url_pattern.search(message):
            continue

        if len(message.split()) < 3:
            continue
        # to lowercase
        message = message.lower()

        # remove garbage
        message = message.replace("\"", "")  # remove "s
        message = message.replace("\n", " ")  # remove newlines
        message = message.replace("\r", " ")  # remove carriage returns

        # remove matching brackets (unmatched ones are likely smileys :-) *cough*
        # should except out when not found.
        index = 0
        try:
            while 1:
                index = message.index("(", index)
                # Remove matching ) bracket
                i = message.index(")", index + 1)
                message = message[0:i] + message[i + 1:]
                # And remove the (
                message = message[0:index] + message[index + 1:]
        except ValueError as e:
            logger.debug(f"filter_message error: {e}", )

        message = message.replace(";", ",")
        message = message.replace("?", " ? ")
        message = message.replace("!", " ! ")
        message = message.replace(".", " . ")
        message = message.replace(",", " , ")
        message = message.replace("'", " ' ")
        message = message.replace(":", " : ")

        # Find ! and ? and append full stops.
        #   message = message.replace(". ", ".. ")
        #   message = message.replace("? ", "?. ")
        #   message = message.replace("! ", "!. ")

        #   And correct the '...'
        #   message = message.replace("..  ..  .. ", ".... ")



        messages.append(message)

    return messages


def checkdict(pyb: "PyborgExperimental") -> str:
    "Check for broken links in the dictionary"
    t = time.time()
    num_broken = 0
    num_bad = 0
    for w in pyb.words.keys():
        wlist = pyb.words[w]
        for i in range(len(wlist) - 1, -1, -1):
            line_idx = wlist[i]['hashval']
            word_num = wlist[i]['index']
            # Nasty critical error we should fix
            if line_idx not in pyb.lines:
                logging.debug("Removing broken link '%s' -> %d" % (w, line_idx))
                num_broken = num_broken + 1
                del wlist[i]
            else:
                # Check pointed to word is correct
                split_line = pyb.lines[line_idx][0].split()
                if split_line[word_num] != w:
                    logging.error("Line '%s' word %d is not '%s' as expected." % (pyb.lines[line_idx][0], word_num, w))
                    num_bad = num_bad + 1
                    del wlist[i]
        if len(wlist) == 0:
            del pyb.words[w]
            pyb.settings.num_words = pyb.settings.num_words - 1
            logging.info("\"%s\" vaped totally" % w)

    output = "Checked dictionary in %0.2fs. Fixed links: %d broken, %d bad." % (time.time() - t, num_broken, num_bad)
    logging.info(output)
    return output


def known2(pyb, words: List[str]) -> str:
    msg = "Number of contexts: "
    for x in words:
        if x in pyb.words:
            c = len(pyb.words[x])
            msg += x + "/" + str(c) + " "
        else:
            msg += x + "/0 "
    return msg


class pyborg:
    def __init__(self) -> None:
        """
        Open the dictionary. Resize as required.
        """
        self.words = {}
        self.lines = {}
        self.num_contexts = 0
        self.num_words = 0

    # TODO: Pegar as  coisas interessantes aqui.
    def do_commands(self, io_module, body: str, args, owner: int) -> None:
        """
        Respond to user commands.
        """
        msg = ""
        command_list = body.split()
        logger.debug("do_commands.command_list: %s", command_list)
        command_list[0] = command_list[0].lower()
        # Guest commands.
        # Version string
        if command_list[0] == "!version":
            msg = self.ver_string

        # How many words do we know?
        elif command_list[0] == "!words":
            num_w = self.settings.num_words
            num_c = self.settings.num_contexts
            num_l = len(self.lines)
            if num_w != 0:
                num_cpw = num_c / float(num_w)  # contexts per word
            else:
                num_cpw = 0.0
            msg = "I know %d words (%d contexts, %.2f per word), %d lines." % (num_w, num_c, num_cpw, num_l)

        # Owner commands
        if owner == 1:
            # Save dictionary
            if command_list[0] == "!save":
                self.save_all()
                msg = "Dictionary saved"

            # Command list
            elif command_list[0] == "!help":
                if len(command_list) > 1:
                    # Help for a specific command
                    cmd = command_list[1].lower()
                    dic = None
                    if cmd in self.commanddict.keys():
                        dic = self.commanddict
                    elif cmd in io_module.commanddict.keys():
                        dic = io_module.commanddict
                    if dic:
                        for i in dic[cmd].split("\n"):
                            io_module.output(i, args)
                    else:
                        msg = "No help on command '%s'" % cmd
                else:
                    for i in self.commandlist.split("\n"):
                        io_module.output(i, args)
                    for i in io_module.commandlist.split("\n"):
                        io_module.output(i, args)

            # Change the max_words setting
            elif command_list[0] == "!limit":
                msg = "The max limit is "
                if len(command_list) == 1:
                    msg += str(self.settings.max_words)
                else:
                    limit = int(command_list[1].lower())
                    self.settings.max_words = limit
                    msg += "now " + command_list[1]

            # Rebuild the dictionary by discarding the word links and
            # re-parsing each line
            elif command_list[0] == "!rebuilddict":
                if self.settings.learning == 1:
                    t = time.time()

                    old_lines = self.lines
                    old_num_words = self.settings.num_words
                    old_num_contexts = self.settings.num_contexts

                    self.words = {}
                    self.lines = {}
                    self.settings.num_words = 0
                    self.settings.num_contexts = 0

                    for k in old_lines.keys():
                        self.learn(old_lines[k][0], old_lines[k][1])

                    msg = "Rebuilt dictionary in %0.2fs. Words %d (%+d), contexts %d (%+d)" % (
                            time.time() - t, old_num_words, self.settings.num_words - old_num_words, old_num_contexts,
                            self.settings.num_contexts - old_num_contexts)

            # Remove rares words
            elif command_list[0] == "!purge":
                t = time.time()
                if len(command_list) == 2:
                    # limite d occurences a effacer
                    c_max = int(command_list[1])
                else:
                    c_max = 0
                number_removed = self.purge(c_max, io_module=io_module)
                msg = "Purge dictionary in %0.2fs. %d words removed" % (time.time() - t, number_removed)

            # Change a typo in the dictionary
            elif command_list[0] == "!replace":
                if len(command_list) < 3:
                    return
                old = command_list[1].lower()
                new = command_list[2].lower()
                msg = self.replace(old, new)

            # Print contexts [flooding...:-]
            elif command_list[0] == "!contexts":
                # This is a large lump of data and should
                # probably be printed, not module.output XXX

                # build context we are looking for
                context = " ".join(command_list[1:])
                context = context.lower()
                if context == "":
                    return
                io_module.output("Contexts containing \"" + context + "\":", args)
                # Build context list
                # Pad it
                context = " " + context + " "
                c = []
                # Search through contexts
                for x in self.lines.keys():
                    # get context
                    ctxt = self.lines[x][0]
                    # add leading whitespace for easy sloppy search code
                    ctxt = " " + ctxt + " "
                    if ctxt.find(context) != -1:
                        # Avoid duplicates (2 of a word
                        # in a single context)
                        if len(c) == 0:
                            c.append(self.lines[x][0])
                        elif c[len(c) - 1] != self.lines[x][0]:
                            c.append(self.lines[x][0])
                x = 0
                while x < 5:
                    if x < len(c):
                        io_module.output(c[x], args)
                    x += 1
                if len(c) == 5:
                    return
                if len(c) > 10:
                    io_module.output("...({} skipped)...".format(len(c) - 10), args)
                x = len(c) - 5
                if x < 5:
                    x = 5
                while x < len(c):
                    io_module.output(c[x], args)
                    x += 1

            # Remove a word from the vocabulary [use with care]
            elif command_list[0] == "!unlearn":
                # build context we are looking for
                context = " ".join(command_list[1:])
                context = context.lower()
                if context == "":
                    return
                print("Looking for: " + context)
                # Unlearn contexts containing 'context'
                t = time.time()
                self.unlearn(context)
                # we don't actually check if anything was
                # done..
                msg = "Unlearn done in %0.2fs" % (time.time() - t)

            # Query/toggle bot learning
            elif command_list[0] == "!learning":
                msg = "Learning mode "
                if len(command_list) == 1:
                    if self.settings.learning == 0:
                        msg += "off"
                    else:
                        msg += "on"
                else:
                    toggle = command_list[1].lower()
                    if toggle == "on":
                        msg += "on"
                        self.settings.learning = 1
                    else:
                        msg += "off"
                        self.settings.learning = 0

            # add a word to the 'censored' list
            elif command_list[0] == "!censor":
                # no arguments. list censored words
                if len(command_list) == 1:
                    if len(self.settings.censored) == 0:
                        msg = "No words censored"
                    else:
                        msg = "I will not use the word(s) %s" % ", ".join(self.settings.censored)
                # add every word listed to censored list
                else:
                    for x in range(1, len(command_list)):
                        if command_list[x] in self.settings.censored:
                            msg += "%s is already censored" % command_list[x]
                        else:
                            self.settings.censored.append(command_list[x].lower())
                            self.unlearn(command_list[x])
                            msg += "done"
                        msg += "\n"

            # remove a word from the censored list
            elif command_list[0] == "!uncensor":
                # Remove everyone listed from the ignore list
                # eg !unignore tom dick harry
                for x in range(1, len(command_list)):
                    try:
                        self.settings.censored.remove(command_list[x].lower())
                        msg = "done"
                    except ValueError as e:
                        logger.exception(e)

            elif command_list[0] == "!alias":
                # no arguments. list aliases words
                if len(command_list) == 1:
                    if len(self.settings.aliases) == 0:
                        msg = "No aliases"
                    else:
                        msg = "I will alias the word(s) %s" % ", ".join(self.settings.aliases.keys())
                # add every word listed to alias list
                elif len(command_list) == 2:
                    if command_list[1][0] != '~':
                        command_list[1] = '~' + command_list[1]
                    if command_list[1] in self.settings.aliases.keys():
                        msg = "Thoses words : %s  are aliases to %s" % (
                                " ".join(self.settings.aliases[command_list[1]]), command_list[1])
                    else:
                        msg = "The alias %s is not known" % command_list[1][1:]
                elif len(command_list) > 2:
                    # create the aliases
                    msg = "The words : "
                    if command_list[1][0] != '~':
                        command_list[1] = '~' + command_list[1]
                    if not (command_list[1] in self.settings.aliases.keys()):
                        self.settings.aliases[command_list[1]] = [command_list[1][1:]]
                        self.replace(command_list[1][1:], command_list[1])
                        msg += command_list[1][1:] + " "
                    for x in range(2, len(command_list)):
                        msg += "%s " % command_list[x]
                        self.settings.aliases[command_list[1]].append(command_list[x])
                        # replace each words by his alias
                        self.replace(command_list[x], command_list[1])
                    msg += "have been aliases to %s" % command_list[1]

            # Quit
            elif command_list[0] == "!quit":
                # Close the dictionary
                self.save_all()
                sys.exit()

            # Save changes
            self.settings.save()
        logger.info(msg)
        if msg != "":
            io_module.output(msg, args)

    # TODO: Adaptar para o banco de dados.
    def process_msg(self, io_module, body, replyrate, learn: int, args, owner=0) -> None:
        """
        Process message 'body' and pass back to IO module with args.
        If owner==1 allow owner commands.
        """
        logger.debug("process_msg: %s", locals())
        # add trailing space so sentences are broken up correctly
        body = body + " "

        # Parse commands
        if body[0] == "!":
            logger.debug("sending do_commands...")
            self.do_commands(io_module, body, args, owner)
            return

        # Filter out garbage and do some formatting
        body = filter_messages(body, self)

        # Learn from input
        if learn == 1:
            self.learn(body)

        # Make a reply if desired
        if randint(0, 99) < int(replyrate):

            message = ""

            # Look if we can find a prepared answer
            for sentence in self.answers.sentences.keys():
                pattern = "^%s$" % sentence
                if re.search(pattern, body):
                    message = self.answers.sentences[sentence][randint(0, len(self.answers.sentences[sentence]) - 1)]
                    break
                else:
                    if body in self.unfilterd:
                        self.unfilterd[body] = self.unfilterd[body] + 1
                    else:
                        self.unfilterd[body] = 0

            if message == "":
                message = self.reply(body)

            # single word reply: always output
            if len(message.split()) == 1:
                io_module.output(message, args)
                return
            # empty do not output
            if message == "":
                return
            # else output
            if owner == 0:
                time.sleep(.2 * len(message))
            io_module.output(message, args)

    # TODO: Adaptar para o banco de dados.
    def replace(self, old: str, new: str) -> str:
        """
        Replace all occuraces of 'old' in the dictionary with
        'new'. Nice for fixing learnt typos.
        """
        try:
            pointers = self.words[old]
        except KeyError:
            return old + " not known."
        changed = 0

        for x in pointers:
            # pointers consist of (line, word) to self.lines
            l = self.words[x['hashval']]  # noqa: E741
            w = self.words[x['index']]
            line = self.lines[l][0].split()
            number = self.lines[l][1]
            if line[w] != old:
                # fucked dictionary
                print("Broken link: %s %s" % (x, self.lines[l][0]))
                continue

            line[w] = new
            self.lines[l][0] = " ".join(line)
            self.lines[l][1] += number
            changed += 1

        if new in self.words:
            self.settings.num_words -= 1
            self.words[new].extend(self.words[old])
        else:
            self.words[new] = self.words[old]
        del self.words[old]
        return "%d instances of %s replaced with %s" % (changed, old, new)

    # TODO: Adaptar para o banco de dados.
    def purge(self, max_contexts: int, io_module=None) -> int:
        "Remove rare words from the dictionary. Returns number of words removed."
        liste = []
        compteur = 0

        for w in self.words.keys():
            digit = 0
            char = 0
            for c in w:
                if c.isalpha():
                    char += 1
                if c.isdigit():
                    digit += 1

            # Compte les mots inferieurs a cette limite
            c = len(self.words[w])
            if c < 2 or (digit and char):
                liste.append(w)
                compteur += 1
                if compteur == max_contexts:
                    break

        if max_contexts < 1:
            # io_module.output(str(compteur)+" words to remove", args)
            if io_module:
                # I'm not gonna pass pyborg.process.args. This breaks the api technically.
                io_module.output("%s words to remove" % compteur, [])

        # supprime les mots
        for w in liste[0:]:
            self.unlearn(w)
        return len(liste[0:])

    # TODO: Adaptar para o banco de dados.
    def unlearn(self, context: str) -> None:
        """
        Unlearn all contexts containing 'context'. If 'context'
        is a single word then all contexts containing that word
        will be removed, just like the old !unlearn <word>
        """
        # Pad thing to look for
        # We pad, so we don't match 'shit' when searching for 'hit', etc.
        context = " " + context + " "
        # Search through contexts
        # count deleted items
        dellist = []
        # words that will have broken context due to this
        wordlist = []
        for x in self.lines.copy().keys():
            # get context. pad
            c = " " + self.lines[x][0] + " "
            if c.find(context) != -1:
                # Split line up
                wlist = self.lines[x][0].split()
                # add touched words to list
                for w in wlist:
                    if w not in wordlist:
                        wordlist.append(w)
                dellist.append(x)
                del self.lines[x]
        words = self.words
        # update links
        for x in wordlist:
            word_contexts = words[x]
            # Check all the word's links (backwards so we can delete)
            for y in range(len(word_contexts) - 1, -1, -1):
                # Check for any of the deleted contexts
                hashval = word_contexts[y]['hashval']
                if hashval in dellist:
                    del word_contexts[y]
                    self.settings.num_contexts = self.settings.num_contexts - 1
            if len(words[x]) == 0:
                del words[x]
                self.settings.num_words = self.settings.num_words - 1
                logger.info(f" \"{x}\" vaped totally")

    async def reply(self, body) -> Optional[str]:
        """
        Reply to a line of text.
        """
        # split sentences into list of words
        _words = body.split(" ")
        words = []
        for i in _words:
            words += i.split()

        if len(words) == 0:
            logger.debug("Did not find any words to reply to.")
            return None


        logger.debug(f"reply: cleaned words: {words}", )
        # Find the rarest word (excluding those unknown)
        index = []
        known = -1
        # The word has to have been seen in already 3 contexts differents for being choosen
        known_min = 3
        for line_index in words:
            logger.debug(f"known_loop: locals: {locals()}")
            if word_db := await Word.get_or_none(word=line_index).prefetch_related("lines"):
                k = len(word_db.lines)
                logger.debug(f"known_loop: {k}??")
            else:
                continue
            if (known == -1 or k < known) and k > known_min:
                index = [line_index]
                known = k
                continue
            elif k == known:
                index.append(line_index)
                continue
        # Index now contains list of rarest known words in sentence
        # index = words

        # def find_known_words(words):
        #     d = dict()
        #     for w in words:
        #         if w in self.words:
        #             logger.debug(self.words[w])
        #             k = len(self.words[w])
        #             d[w] = k
        #     logger.debug("find_known_words: %s", d)
        #     idx = [x for x,y  in d.items() if y > 3]
        #     logger.debug("find_known_words: %s", idx)
        #     return idx

        # index = find_known_words(words)

        if len(index) == 0:
            logger.debug("No words with atleast 3 contexts were found.")
            logger.debug(f"reply:index: {index}")
            return ""

        # Begin experimental NLP code
        def weight(pos: str) -> int:
            """Takes a POS tag and assigns a weight
            New: doubled the weights in 1.4"""
            lookup = {"NN": 8, "NNP": 10, "RB": 4, "NNS": 6, "NNPS": 10}
            try:
                ret = lookup[pos]
            except KeyError:
                ret = 2
            return ret

        def _mappable_nick_clean(pair: Tuple[str, str]) -> Tuple[str, int]:
            "mappable weight apply but with shortcut for #nick"
            word, pos = pair
            if word == "#nick":
                comp_weight = 1
            else:
                comp_weight = weight(pos)
            return (word, comp_weight)

        def map_spacy_pos_to_nltk(spacy_tag, text):
            mapping = {'ADJ': 'JJ',  # Adjective
                       'ADP': 'IN',  # Adposition (preposition/subordinating conjunction)
                       'ADV': 'RB',  # Adverb
                       'AUX': 'VB',  # Auxiliary
                       'CONJ': 'CC',  # Conjunction
                       'DET': 'DT',  # Determiner
                       'INTJ': 'UH',  # Interjection
                       'NOUN': 'NN',  # Noun, singular or mass
                       'NUM': 'CD',  # Numeral
                       'PART': 'RP',  # Particle
                       'PRON': 'PRP',  # Pronoun
                       'PROPN': 'NNP',  # Proper noun, singular
                       'PUNCT': text,  # Punctuation
                       'SCONJ': 'IN',  # Subordinating conjunction
                       'SYM': 'SYM',  # Symbol
                       'VERB': 'VB',  # Verb
                       'X': 'X',  # Other
                       }
            return mapping.get(spacy_tag, spacy_tag)  # else:  #     return spacy_tag

        if nltk:
            # uses punkt
            tokenized = nltk.tokenize.casual.casual_tokenize(body)
            # uses averaged_perceptron_tagger
            nlp = spacy.load("./minify_model")
            tagged = [(token.text, map_spacy_pos_to_nltk(token.pos_, token.text)) for token in nlp(body)]
            # tagged2 = nltk.pos_tag(tokenized)
            weighted_choices = list(map(_mappable_nick_clean, tagged))
            population = [val for val, cnt in weighted_choices for i in range(cnt)]
            word = random.choice(population)
            # make sure the word is known
            counter = 0

            word_list = random.choices(population, k=len(population))

            word_db = await Word.get_word_list(word_list)

            word = word_db.word

            logger.debug(f"Ran choice {counter} times", )
        else:
            word = index[randint(0, len(index) - 1)]

        sentence = [word]
        done = 0
        while done == 0:
            # create a dictionary wich will contain all the words we can found before the "chosen" word
            pre_words = {"": 0}
            # this is for prevent the case when we have an ignore_listed word
            word = str(sentence[0].split(" ")[0])
            word_db = await Word.get_or_none(word=word).prefetch_related("lines")
            word_line_index = await word_db.greb_lines_and_indexs()
            for x in range(0, len(word_db.lines) - 1):
                reference = word_line_index[x]
                logger.debug(locals())
                logger.debug(f'trying to unpack: {reference}', )
                line_hashval = reference[0]  # noqa: E741
                line_index = reference[1]
                context = line_hashval.content
                num_context = line_hashval.num_context
                cwords = context.split()
                # if the word is not the first of the context, look the previous one
                if cwords[line_index] != word:
                    print(context)
                if line_index or line_index == 0:
                    # look if we can found a pair with the choosen word, and the previous one
                    if len(sentence) > 1 and len(cwords) > line_index + 1:
                        if sentence[1] != cwords[line_index + 1]:
                            continue

                    # if the word is in ignore_list, look the previous word
                    look_for = cwords[line_index - 1]

                    # saves how many times we can found each word
                    if look_for not in pre_words:
                        pre_words[look_for] = num_context
                    else:
                        pre_words[look_for] += num_context

                else:
                    pre_words[""] += num_context
            # Sort the words
            liste = list(pre_words.items())  # this is a view in py3
            liste.sort(key=lambda x: x[1])
            numbers = [liste[0][1]]
            for x in range(1, len(liste)):
                numbers.append(liste[x][1] + numbers[x - 1])

            # take one them from the list ( randomly )
            mot = randint(0, numbers[len(numbers) - 1])
            for x in range(0, len(numbers)):
                if mot <= numbers[x]:
                    mot = liste[x][0]
                    break

            # if the word is already choosen, pick the next one
            while mot in sentence:
                x += 1
                if x >= len(liste) - 1:
                    mot = ''
                logger.info(f"the choosening: {liste[x]}", )
                mot = liste[x][0]

            # logger.debug("mot1: %s", len(mot))
            mot = mot.split()
            mot.reverse()
            if mot == []:
                done = 1
            else:
                list(map((lambda x: sentence.insert(0, x)), mot))

        pre_words = sentence
        sentence = sentence[-2:]

        # Now build sentence forwards from "chosen" word

        # We've got
        # cwords:    ... cwords[w-1] cwords[w]   cwords[w+1] cwords[w+2]
        # sentence:  ... sentence[-2]    sentence[-1]    look_for    look_for ?

        # we are looking, for a cwords[w] known, and maybe a cwords[w-1] known, what will be the cwords[w+1] to choose.
        # cwords[w+2] is need when cwords[w+1] is in ignored list
        done = 0
        while done == 0:
            # create a dictionary wich will contain all the words we can found before the "chosen" word
            post_words = {"": 0}
            word = str(sentence[-1].split(" ")[-1])
            word_db = await Word.get_or_none(word=word).prefetch_related("lines")
            word_line_index = await word_db.greb_lines_and_indexs()
            for x in range(0, len(word_db.lines)):
                reference = word_line_index[x]
                line_hashval = reference[0]  # noqa: E741
                line_index = reference[1]
                context = line_hashval.content
                num_context = line_hashval.num_context
                cwords = context.split()
                # look if we can found a pair with the choosen word, and the next one
                if len(sentence) > 1:
                    if sentence[len(sentence) - 2] != cwords[line_index - 1]:
                        continue

                if line_index < len(cwords) - 1:
                    # if the word is in ignore_list, look the next word
                    look_for = cwords[line_index + 1]

                    if look_for not in post_words:
                        post_words[look_for] = num_context
                    else:
                        post_words[look_for] += num_context
                else:
                    post_words[""] += num_context
            # Sort the words
            liste = list(post_words.items())
            liste.sort(key=lambda x: x[1])
            numbers = [liste[0][1]]

            for x in range(1, len(liste)):
                numbers.append(liste[x][1] + numbers[x - 1])

            # take one them from the list ( randomly )
            mot = randint(0, numbers[len(numbers) - 1])
            for x in range(0, len(numbers)):
                if mot <= numbers[x]:
                    mot = liste[x][0]
                    break

            x = -1
            while mot in sentence:
                x += 1
                if x >= len(liste) - 1:
                    mot = ''
                    break
                mot = liste[x][0]

            # logger.debug("mot2: %s", len(mot))
            mot = mot.split()
            if mot == []:
                done = 1
            else:
                list(map(lambda x: sentence.append(x), mot))
        sentence = pre_words[:-2] + sentence
        # this seems bogus? how does this work???

        # Replace aliases
        for x in range(0, len(sentence)):
            if sentence[x][0] == "~":
                sentence[x] = sentence[x][1:]

        # Insert space between each words
        list(map((lambda x: sentence.insert(1 + x * 2, " ")), range(0, len(sentence) - 1)))

        # correct the ' & , spaces problem
        # code is not very good and can be improve but does his job...
        for x in range(0, len(sentence)):
            if sentence[x] == "'":
                sentence[x - 1] = ""
                sentence[x + 1] = ""
            if sentence[x] == ",":
                sentence[x - 1] = ""
        logger.debug(f"final locals: {locals()}", )
        return "".join(sentence)

    async def learn(self, body: List[str], num_context: int = 1) -> None:
        """
        Lines should be cleaned (filter_message()) before passing
        to this.
        """

        async def learn_line(body: str, num_context: int) -> None:
            """
            Learn from a sentence.
            nb: there is a closure here...
            """
            logger.debug("entering learn_line")
            if nltk:
                words = nltk.word_tokenize(body)
            else:
                words = body.split()
            # Ignore sentences of < 1 words XXX was <3
            if len(words) < 1:
                return

            # voyelles = "aÃ Ã¢eÃ©Ã¨ÃªiÃ®Ã¯oÃ¶Ã´uÃ¼Ã»y"
            voyelles = "aeiouy"
            logger.debug(f"reply:learn_line:words: {words}")
            for x in range(0, len(words)):

                nb_voy = 0
                digit = 0
                char = 0
                for c in words[x]:
                    if c in voyelles:
                        nb_voy += 1
                    if c.isalpha():
                        char += 1
                    if c.isdigit():
                        digit += 1

                # if len(words[x]) > 13 or (((nb_voy * 100) / len(words[x]) < 26) and len(words[x]) > 5) or (
                #         char and digit) or (words[x] in self.words) == 0:
                #     logger.debug("reply:learn_line: Bailing because reasons?")
                #     return
                # elif "-" in words[x] or "_" in words[x]:
                #     words[x] = "#nick"

            clean_body = " ".join(words)
            hashval = mmh3.hash(bytes(clean_body, "utf-8"), signed=False)
            logger.debug(hashval)
            # Check context isn't already known
            line = await Line.get_or_none(hashval=hashval)
            if not line:
                line = await Line.create(hashval=hashval, content=clean_body, num_context=num_context)
                # Add a link for each word
                for i, word in enumerate(words):
                    word_db = await Word.get_or_none(word=word)
                    if word_db:
                        await word_db.lines.add(line)
                        word_db.indexs.append({"hashval": hashval, "index": i})
                        # word_line = await WordLine.create(word=word_db, line=line, index=i)
                    else:
                        word_db = await Word.create(word=word)
                        await word_db.lines.add(line)
                        word_db.indexs.append({"hashval": hashval, "index": i})
                        # word_line = await WordLine.create(word=word_db, line=line, index=i)
                    await line.words.add(word_db)
                    await word_db.save()
                await line.save()

            else:
                await Line.filter(hashval=hashval).update(num_context=line.num_context + 1)


        # Split body text into sentences and parse them
        # one by one.
        body += " "
        logger.debug(f"reply:replying to {body}", )
        # map ( (lambda x : learn_line(self, x, num_context)), body.split(". "))
        for part in body:
            await learn_line(part, num_context)
