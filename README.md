# WikiSearch
Wikipedia Scraping for section and links summary

Current version requires typing in a link first.

Sections organized into major sections and sub-sections titled "Section" and "Sub-Section" respectively. 
Links are printed first and common words second. 

Current Version sometimes print words part of a few sentences on a major section's introduction (e.g. further information). A check should added for the sentence size or other indication of small introduction. 

Table is filtered out because of highly repeated words that are not in sentences. https://en.wikipedia.org/wiki/Dog would print species abbreviation and names that are not in the first summary.

Ends if "References" section is spotted. Articles with no "References" section still work just without printing "Common Words" for last section. Project spec does not clarify which section program should exit at.
