# strongbad_email

I love strongbad emails; and I want more. I have [scraped](scraper/) the text of every strongbad email from the [homestarrunner wiki](http://www.hrwiki.org/). If someone were to write a GAN to create more, we could send them to the Brothers Chaps and maybe they'd make them?

_Maybe_ I'll work on that GAN but that doesn't sound a whole lot like something I'd do.

## The Data

This is a simple [SQLite database](strongbad_emails.db) with one table:

- `id`: Integer email ID.
- `title`: The email title.
- `message`: The content of the email that Strongbad answered, not including any of Strongbad's subsequent annotations, alterations, etc.
- `homestarrunner_url`: The URL for the email on homestarrunner.
- `hrwiki_url`: The URL for the email on hrwiki.
