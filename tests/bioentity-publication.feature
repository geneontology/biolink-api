Feature: Publication association queries that return a list of associations

## Publication to Disease associations

    Scenario: User queries for diseases associated with a publication
        Given a path "/bioentity/publication/PMID:19652879/diseases"
        then the JSON should have some JSONPath "associations[*].object.label" with "string" "congenital factor XI deficiency"
        then the JSON should have some JSONPath "associations[*].provided_by" containing "string" "https://data.monarchinitiative.org/ttl/clinvar.ttl"

## Publication to Gene associations

    Scenario: User queries for genes associated with a publication
        Given a path "/bioentity/publication/PMID:11751940/genes"
        then the JSON should have some JSONPath "associations[*].object.id" with "string" "MGI:88336"
        then the JSON should have some JSONPath "associations[*].object.id" with "string" "RGD:708418"
        then the JSON should have some JSONPath "associations[*].object.id" with "string" "MGI:88337"

## Publication to Phenotype associations

    Scenario: User queries for genes associated with a publication
        Given a path "/bioentity/publication/PMID:11751940/phenotypes"
        then the JSON should have some JSONPath "associations[*].object.id" with "string" "MP:0004771"
        then the JSON should have some JSONPath "associations[*].object.label" with "string" "increased anti-single stranded DNA antibody level"
        then the JSON should have some JSONPath "associations[*].provided_by" containing "string" "https://data.monarchinitiative.org/ttl/mgi_slim.ttl"

## Publication to Genotype associations

    Scenario: User queries for genes associated with a publication
        Given a path "/bioentity/publication/PMID:20220848/genotypes"
        then the JSON should have some JSONPath "associations[*].object.taxon.label" with "string" "Drosophila melanogaster"
        then the JSON should have some JSONPath "associations[*].object.id" with "string" "MONARCH:FBgeno426941"
        then the JSON should have some JSONPath "associations[*].provided_by" containing "string" "https://data.monarchinitiative.org/ttl/flybase.ttl"

## Publication to Model associations

    Scenario: User queries for genes associated with a publication
        Given a path "/bioentity/publication/PMID:11181576/models"
        then the JSON should have some JSONPath "associations[*].object.taxon.label" with "string" "Homo sapiens"
        then the JSON should have some JSONPath "associations[*].object.id" with "string" "Coriell:GM05823"
        then the JSON should have some JSONPath "associations[*].object.label" with "string" "NIGMS-GM05823"
        then the JSON should have some JSONPath "associations[*].provided_by" containing "string" "https://data.monarchinitiative.org/ttl/coriell.ttl"

## Publication to Variant ssociations

    Scenario: User queries for genes associated with a publication
        Given a path "/bioentity/publication/PMID:11751940/variants"
        then the JSON should have some JSONPath "associations[*].object.taxon.label" with "string" "Rattus norvegicus"
        then the JSON should have some JSONPath "associations[*].object.id" with "string" "RGD:708418"
        then the JSON should have some JSONPath "associations[*].object.label" with "string" "Cd40lg"
        then the JSON should have some JSONPath "associations[*].provided_by" containing "string" "https://data.monarchinitiative.org/ttl/ncbigene.ttl"
