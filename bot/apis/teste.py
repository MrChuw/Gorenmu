import aiorequests
import html

word = "teste"
url: str = "http://www.dicio.com.br"

url = f"{url}/{word}"
print(url)


def exists(word: str) -> bool:
    async def exists1(word) -> bool:
        response = await aiorequests.get(url, res_method="text")
        print(response)
        text = html.unescape(response)
        print(text)
        start = text.find("<h1")
        print(start)
        if start != -1:
            start += len("<h1")
        start = text.find(">", start) + 1
        end = text.find("</h1>", start)
        find = text[start:end] if -1 < start < end else text
        return find.lower() == text.lower()

    return exists1(word)


print(exists(word))
