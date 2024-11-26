# Construct the APA citation
apa_citation <- function(author, year, title, journal, volume, issue, pages, doi){
  paste(
    author, 
    paste0("(", year, ")."),
    title, 
    paste0("*", journal, "*, ", volume, "(", issue, "), ", pages, "."),
    doi
  )
}


template_publication <- function(){
"---
title: \"{{title}}\"
type: \"article\"
author: \"{{author}}\"
year: \"{{year}}\"
doi: \"{{doi}}\"
categories: []
---

# Abstract
{{abstract}}

# Citation (APA)
{{citation}}
"

}


qmd_content <- function(template, title, author, year, doi, abstract, citation, key){

  # Replace placeholders in the template
  qmd_file <- template |>
    str_replace_all(c("\\{\\{title\\}\\}" = title, 
                      "\\{\\{author\\}\\}" = author,
                      "\\{\\{year\\}\\}" = year,
                      "\\{\\{doi\\}\\}" = doi,
                      "\\{\\{abstract\\}\\}" = ifelse(!is.na(abstract), abstract, "No abstract available."),
                      "\\{\\{citation\\}\\}" = citation))

  # Write to a .qmd file
  file_name <- paste0("publications/", key, ".qmd")
  writeLines(qmd_file, file_name)

}


