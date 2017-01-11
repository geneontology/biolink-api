Feature: Association queries return lists of associations

## General Associations

 Scenario: Client queries for all annotations in Monotremes (e.g. Duck billed platypus)
    Given a path [http://api.monarchinitiative.org/api/association/find/?subject_taxon=NCBITaxon:9255&rows=10&fl_excludes_evidence=true&page=1](http://api.monarchinitiative.org/api/association/find/?subject_taxon=NCBITaxon:9255&rows=10&fl_excludes_evidence=true&page=1)
    when the content is converted to JSON
      then the JSON should have some JSONPath "associations[*].subject.taxon.label" with "string" "Ornithorhynchus anatinus"
      then the JSON should have some JSONPath "associations[*].object.label" with "string" "Asthma"
Feature: Association queries work as expected

## Gene-Phenotype Associations

 Scenario: User queries for mouse genes with abnormal Bowman membrane phenotype
    Given a path [http://api.monarchinitiative.org/api/association/find/gene/phenotype/?subject_taxon=NCBITaxon:10090&rows=10&object=MP:0008521](http://api.monarchinitiative.org/api/association/find/gene/phenotype/?subject_taxon=NCBITaxon:10090&rows=10&object=MP:0008521)
     then the content should contain "abnormal Bowman membrane"
    when the content is converted to JSON
      then the JSON should have some JSONPath "phenotype_associations[*].subject.id" with "string" "MGI:1342287"
      and the JSON should have some JSONPath "phenotype_associations[*].object.id" with "string" "MP:0008521"
      and the JSON should have some JSONPath "phenotype_associations[*].object.label" with "string" "abnormal Bowman membrane"
Feature: Association queries return lists of associations

## General Associations

 Scenario: Client wants human and mouse genes with cardiovascular phenotypes, using a HPO ID
    Given a path [http://api.monarchinitiative.org/api/association/find/gene/phenotype?subject_taxon=NCBITaxon:40674&object=HP:0001626&fl_excludes_evidence=true&page=1](http://api.monarchinitiative.org/api/association/find/gene/phenotype?subject_taxon=NCBITaxon:40674&object=HP:0001626&fl_excludes_evidence=true&page=1)
    when the content is converted to JSON
      then the JSON should have some JSONPath "associations[*].object.id" with "string" "HP:0011025"  ## CLOSURE

 Scenario: Client wants human and mouse genes with cardiovascular phenotypes, using an MP ID
    Given a path [http://api.monarchinitiative.org/api/association/find/gene/phenotype?subject_taxon=NCBITaxon:40674&object=MP:0005385&fl_excludes_evidence=true&page=1](http://api.monarchinitiative.org/api/association/find/gene/phenotype?subject_taxon=NCBITaxon:40674&object=MP:0005385&fl_excludes_evidence=true&page=1)
    when the content is converted to JSON
      then the JSON should have some JSONPath "associations[*].subject.taxon.label" with "string" "Ornithorhynchus anatinus"
      then the JSON should have some JSONPath "associations[*].object.label" with "string" "Asthma"

Feature: bioentity routes work as expected

These routes (`bioentity`) provide a way to query for domain-specific
objects such as genes, diseases, etc, as well as for associations
between these entities

## Genes
 
 Scenario: User fetches all information on a human gene
    Given a path [http://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:84570](http://api.monarchinitiative.org/api/bioentity/gene/NCBIGene:84570)
     then the content should contain "COL25A1"
    when the content is converted to JSON
      then the JSON should have the top-level property "id"
      and the JSON should have a JSONPath "homology_associations[*].object"
      and the JSON should have a JSONPath "homology_associations[*].object.id"
      and the JSON should have some JSONPath "homology_associations[*].object.label" with "string" "col25a1"

 Scenario: User fetches all information on a mouse gene
    Given a path [http://api.monarchinitiative.org/api/bioentity/gene/MGI:1342287](http://api.monarchinitiative.org/api/bioentity/gene/MGI:1342287)
     then the content should contain "Klf4"
    when the content is converted to JSON
      then the JSON should have the top-level property "id"
      and the JSON should have some JSONPath "phenotype_associations[*].object.id" with "string" "MP:0008521"
      and the JSON should have some JSONPath "phenotype_associations[*].object.label" with "string" "abnormal Bowman membrane"

## TODO: ensure label populated in scigraph call

 Scenario: User fetches all information on the same mouse gene, using an ENSEMBL ID
    Given a path [http://api.monarchinitiative.org/api/bioentity/gene/ENSEMBL:ENSMUSG00000003032](http://api.monarchinitiative.org/api/bioentity/gene/ENSEMBL:ENSMUSG00000003032)
     then the content should contain "Klf4"
    when the content is converted to JSON
      then the JSON should have some JSONPath "phenotype_associations[*].subject.id" with "string" "MGI:1342287"
      and the JSON should have some JSONPath "phenotype_associations[*].object.id" with "string" "MP:0008521"
      and the JSON should have some JSONPath "phenotype_associations[*].object.label" with "string" "abnormal Bowman membrane"

Feature: Phenotype entity queries work as expected

TODO

## Phenotypes

 Scenario: User queries for mouse genes with abnormal Bowman membrane phenotype
    Given a path [http://api.monarchinitiative.org/api/bioentity/phenotype/MP:0008521](http://api.monarchinitiative.org/api/bioentity/phenotype/MP:0008521)
     then the content should contain "foo"