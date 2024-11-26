## libs ----
library(bib2df)
library(dplyr)
library(stringr)

## funs ----
source("fun.R")

## dat ----
bib_data <- bib2df("my_publications.bib")
names(bib_data) <- tolower(names(bib_data))

template <- template_publication()

for (i in 1:nrow(bib_data)) {
  # Extract fields
  
  key <- bib_data$bibtexkey[i]
  title <- bib_data$title[i]
  author <- paste(bib_data$author[[i]], collapse = ", ")
  year <- bib_data$year[i]
  journal <- bib_data$journal[i]
  volume <- bib_data$volume[i]
  issue <- bib_data$issue[i]
  pages <- bib_data$pages[i]
  doi <- bib_data$doi[i]
  
  abstract <- bib_data$abstract[i]
  citation <- apa_citation(author, year, title, journal, volume, issue, pages, doi)
  
  qmd_content(template, title, author, year, doi, abstract, citation, key)
  
  
}





  
