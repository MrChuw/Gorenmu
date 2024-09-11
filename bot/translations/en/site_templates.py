from textwrap import dedent



class EnSiteTemplates:
    language_code: dict[str, str] = {"en": "en"}
    link: str = '/en/'
    home: str = 'Home'
    commands: str = 'Commands'
    table: list[str] = ['Command Name', 'Description', 'Extras']
    name: str = 'English'
    home_index_template: str = dedent(f"""
    ---
    date: 2024-09-09
    ---
    
    # Home
    # I still don't know what to put here.

    [The commands are here]({commands.lower()}/index.md)
    """).lstrip('\n')

    blog_index_template: str = dedent("""
    ---
    date: 2024-09-09
    ---
    
    # Changelogs
    """).lstrip('\n')

    authors = [
            {
                'reference': "mrchuw",
                'name': "Mrchuw",
                'description_tipe': 'Creator',
                'avatar': "https://github.com/mrchuw.png",
            },
            {  # Example
                'reference': "squidfunk",
                'name': "Martin Donath",
                'description_tipe': 'Contributor',
                'avatar': "https://github.com/squidfunk.png",
            },
    ]
    authors_descriptions = {
            "Creator": "Creator",
            "Maintainer": "Maintainer",
            "Contributor": "Contributor",
    }

    changelogs = [
            dedent("""
            ---
            date:
              created: 2024-09-11T00:39:15.349-03:00
              updated: 2024-09-11T00:39:15.349-03:00
            authors:
              - mrchuw
            categories:
              - afk
              - isafk
              - rafk
            slug: Changelog-1
            title: Changelog 1
            ---
            
            # Changelog - 
            
            <!-- more -->
            
            """).lstrip('\n'),
    ]





