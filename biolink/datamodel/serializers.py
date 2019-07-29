from flask_restplus import fields
from biolink.api.restplus import api


# todo: split this into modules
# TODO: convert to marshmallow

# Solr

search_result = api.model('SearchResult', {
    'numFound': fields.Integer(description='total number of associations matching query'),
    'docs': fields.List(fields.Raw, description='solr docs'),
    'facet_counts': fields.Raw(description='Mapping between field names and association counts'),
    'highlighting': fields.Raw(description='Mapping between id and solr highlight')
})

autocomplete_result = api.model('AutocompleteResult', {
    'id': fields.String(description='curie formatted id'),
    'label': fields.List(fields.String, description='primary label (rdfs:label)'),
    'match': fields.String(description='matched part of document (may be primary label, synonym, id, etc)'),
    'category': fields.List(fields.String, description='node categories'),
    'taxon': fields.String(description='taxon as NCBITaxon curie'),
    'taxon_label': fields.String(description='taxon label'),
    'highlight': fields.String(description='solr highlight'),
    'has_highlight': fields.Boolean(description='True if highlight can be interpreted as html, else False')
})

autocomplete_results = api.model('AutocompleteResults', {
    'docs': fields.List(fields.Nested(autocomplete_result),
                        description='list of AutocompleteResult docs'),
})

lay_autocomplete = api.model('LayAutocomplete', {
    'id': fields.String(description='curie formatted id'),
    'label': fields.String(description='primary label (rdfs:label)'),
    'matched_synonym': fields.String(description='matched synonym'),
    'highlight': fields.String(description='solr highlight')
})

lay_results = api.model('LayResults', {
    'results': fields.List(fields.Nested(lay_autocomplete),
                        description='list of AutocompleteResult docs'),
})


## BBOP/OBO Graphs

abstract_property_value = api.model('AbstractPropertyValue', {
    'val': fields.String(readOnly=True, description='value part'),
    'pred': fields.String(readOnly=True, description='predicate (attribute) part'),
    'xrefs': fields.List(fields.String, description='Xrefs provenance for property-value'),
})

synonym_property_value = api.inherit('SynonymPropertyValue', abstract_property_value, {
})

summary_property_value = api.inherit('SummaryPropertyValue', abstract_property_value, {
})

association_property_value = api.inherit('AssociationPropertyValue', abstract_property_value, {
})


node = api.model('Node', {
    'id': fields.String(readOnly=True, description='ID or CURIE'),
    'lbl': fields.String(readOnly=True, description='human readable label, maps to rdfs:label'),
    'meta': fields.Raw(description='metadata about the Node')
})

edge = api.model('Edge', {
    'sub': fields.String(readOnly=True, description='Subject (source) Node ID'),
    'pred': fields.String(readOnly=True, description='Predicate (relation) ID'),
    'obj': fields.String(readOnly=True, description='Object (target) Node ID'),
    'meta': fields.Raw(description='metadata about the Edge')
})

bbop_graph = api.model('Graph', {
    'nodes': fields.List(fields.Nested(node), description='All nodes in graph'),
    'edges': fields.List(fields.Nested(edge), description='All edges in graph'),
})

named_object_core = api.model('NamedObjectCore', {
    'id': fields.String(readOnly=True, description='ID or CURIE e.g. MGI:1201606', required=True),
    'label': fields.String(readOnly=True, description='RDFS Label'),
    'iri': fields.String(readOnly=True, description='IRI'),
    'category': fields.List(fields.String(readOnly=True, description='Type of object'))
})


named_object = api.inherit('NamedObject', named_object_core, {
    'description': fields.String(readOnly=True, description='Descriptive text for the entity. For ontology classes, this will be a definition.'),
    'types': fields.List(fields.String(readOnly=True, description='Type of object (direct)')),
    'synonyms': fields.List(fields.Nested(synonym_property_value), description='list of synonyms or alternate labels'),
    'deprecated': fields.Boolean(description='True if the node is deprecated/obsoleted.'),
    'replaced_by': fields.List(fields.String(readOnly=True, description='Direct 1:1 replacement (if named object is obsoleted)')),
    'consider': fields.List(fields.String(readOnly=True, description='Potential replacement object (if named object is obsoleted)')),
})

entity_reference = api.model('EntityReference', {
    'id': fields.String(readOnly=True, description='ID or CURIE e.g. MGI:1201606'),
    'label': fields.String(readOnly=True, description='RDFS Label'),
})

relation = api.inherit('Relation', named_object, {
})

relation_ref = api.inherit('RelationRef', named_object_core, {
    'inverse': fields.Boolean(description='is relation inverted', default=False)
})

publication = api.inherit('Publication', named_object, {
    # authors etc
})


# todo: inherits
taxon = api.model('Taxon', {
    'id': fields.String(readOnly=True, description='CURIE ID, e.g. NCBITaxon:9606'),
    'label': fields.String(readOnly=True, description='RDFS Label')
})

bio_object_core = api.inherit('BioObjectCore', named_object_core, {
    'taxon': fields.Nested(taxon, description='Taxon to which the object belongs'),
    
})

bio_object = api.inherit('BioObject', named_object, {
    'taxon': fields.Nested(taxon, description='Taxon to which the object belongs'),
    'association_counts': fields.Raw(description='association counts'),
    'xrefs': fields.List(fields.String, description='Database cross-references. These are usually CURIEs, but may also be URLs. E.g. ENSEMBL:ENSG00000099940 '),
})

disease_object = api.inherit('DiseaseObject', bio_object, {
    'inheritance': fields.List(fields.Nested(named_object_core), description='Inheritance for object'),
    'clinical_modifiers': fields.List(fields.Nested(named_object_core), description='Clinical modifiers such as age of onset, pace of progression, and temporal patterns'),
})

# Assoc

annotation_extension = api.model('AnnotationExtension', {
    'relation_chain': fields.List(fields.Nested(relation), description='Relationship type. If more than one value, interpreted as chain'),
    'filler': fields.Nested(named_object, description='Extension interpreted as OWL expression (r1 some r2 some .. some filler).'),
})

association = api.model('Association', {
    'id': fields.String(readOnly=True, description='Association/annotation unique ID', required=True),
    'type': fields.String(readOnly=True, description='Type of association, e.g. gene-phenotype'),
    'subject': fields.Nested(bio_object_core, description='Subject of association (what it is about), e.g. ClinVar:nnn, MGI:1201606', required=True),
    'subject_extensions': fields.List(fields.Nested(annotation_extension, description='Additional properties of the subject in the context of this association.')),
    'object': fields.Nested(bio_object_core, description='Object (sensu RDF), aka target, e.g. HP:0000448, MP:0002109, DOID:14330', required=True),
    'object_extensions': fields.List(fields.Nested(annotation_extension, description='Additional properties of the object in the context of this association. See http://www.biomedcentral.com/1471-2105/15/155')),
    'relation': fields.Nested(relation_ref, description='Relationship type connecting subject and object', required=True),
    'slim': fields.List(fields.String, description='Objects mapped to a slim'),
    'negated': fields.Boolean(description='True if association is negated'),
    'qualifiers': fields.List(fields.String, description='Qualifier on the association'),
    'evidence_graph': fields.Nested(bbop_graph, description='An indirect association is a join between two or more direct assocations, e.g. gene to disease via ortholog. We record the full set of associations as a graph object'),
    'evidence_types': fields.List(fields.Nested(named_object), description='Evidence types (ECO classes) extracted from evidence graph'),
    'provided_by': fields.List(fields.String, description='Provider of association, e.g. Orphanet, ClinVar'),
    'publications': fields.List(fields.Nested(publication), description='Publications supporting association, extracted from evidence graph')
})

# For example, via homology
chained_association = api.model('ChainedAssociation', {
    'proximal_association': fields.Nested(association, description='immediate association, between subject and intermediate object'),
    'distal_associations': fields.List(fields.Nested(association), description='Associations where the intermediate object is the subject')
})

slimmed_association = api.model('SlimmedAssociation', {
    'associations': fields.List(fields.Nested(association, description='immediate association, between subject and intermediate object')),
    'subject': fields.String(description='subject of association (e.g. gene)'),
    'slim': fields.String(description='Slimmed term')
})

compact_association_set = api.model('CompactAssociationSet', {
    'subject': fields.String(description='Subject of association (what it is about), e.g. MGI:1201606', required=True),
    'relation': fields.String(description='Relationship type connecting subject and object list', required=True),
    'objects': fields.List(fields.String, description='List of O, for a given (S,R) pair, yielding (S,R,O) triples. E.g. list of MPs for (MGI:nnn, has_phenotype)', required=True),
})

# A search result that returns a set of associations
association_results = api.inherit('AssociationResults', search_result, {
    'associations': fields.List(fields.Nested(association), description='Complete representation of full association object, plus evidence'),
    'compact_associations': fields.List(fields.Nested(compact_association_set), description='Compact representation in which objects (e.g. phenotypes) are collected for subject-predicate pairs'),
    'objects': fields.List(fields.String, description='List of distinct objects used')
})

d2p_association = api.inherit('D2PAssociation', association, {
    'frequency': fields.Nested(entity_reference,
                               description='Frequency of phenotype '
                                           'in patients with disease',
                               required=False),
    'onset': fields.Nested(entity_reference,
                           description='Onset of phenotype in disease process',
                           required=False)
})

# A search result that returns a set of associations
# plus specific fields for disease to phenotype (frequency and onset)
d2p_association_results = api.inherit('D2PAssociationResults', search_result, {
    'associations': fields.List(fields.Nested(d2p_association),
                                description='Complete representation of full disease '
                                            'to phenotype association, plus evidence'),
    'compact_associations': fields.List(fields.Nested(compact_association_set),
                                        description='Compact representation in which objects '
                                                    '(e.g. phenotypes) are collected '
                                                    'for subject-predicate pairs'),
    'objects': fields.List(fields.String, description='List of distinct objects used')
})


#############
# Bio Objects

sequence_position = api.model('SequencePosition', {
    'position': fields.Integer,
    'reference': fields.String
})

sequence_location = api.inherit('SequenceLocation', bio_object, {
    'start': fields.Nested(sequence_position),
    'end': fields.Nested(sequence_position),
    'phase': fields.Integer(descript="Indicates where the feature begins with reference to the reading frame (0,1,2)."),
    'score': fields.Integer(descript="The score of the feature, a floating point number."),
    'strand': fields.Integer (description="Strand direction: 1=='+', -1=='-', 0 or null infers unknown."),
})

seq = api.inherit('Seq', bio_object, {
    'alphabet': fields.String(description='one of: DNA, RNA or AA'),
    'residues': fields.String(description='string representing sequence of residues'),
    'md5checksum': fields.String(description='checksum'),
    'seqlen': fields.String(description='length of sequence'),
})

sequence_feature = api.inherit('SequenceFeature', bio_object, {
    'locations': fields.List(fields.Nested(sequence_location)),
    'seq': fields.Nested(seq),
    'homology_associations': fields.List(fields.Nested(association)),
})

chromosome = api.inherit('Chromosome', bio_object, {
})

gene_product = api.inherit('GeneProduct', bio_object, {
    'sequence_features' : fields.List(fields.Nested(sequence_feature), description='Sequence feature representing this particular instance on a genome'),
    'genes': fields.List(fields.Nested(entity_reference), description='References to any gene objects that have this as product')
})

exon = api.inherit('Exon', bio_object, {
    'sequence_features' : fields.List(fields.Nested(sequence_feature), description='Sequence feature representing this particular instance on a genome'),
    'genes': fields.List(fields.Nested(entity_reference), description='References to any gene objects that have this exon in any of their transcripts')
})

cds = api.inherit('CDS', bio_object, {
    'sequence_features' : fields.List(fields.Nested(sequence_feature), description='Sequence feature representing this particular instance on a genome'),
    'genes': fields.List(fields.Nested(entity_reference), description='References to any gene objects that have this exon in any of their transcripts')
})

regulatory_element = api.inherit('RegulatoryElement', bio_object, {
    'sequence_features' : fields.List(fields.Nested(sequence_feature), description='Sequence feature representing this particular instance on a genome'),
    'targets': fields.List(fields.Nested(entity_reference), description='References to any gene objects whose expression is regulated by this element')
})

transcript = api.inherit('Transcript', bio_object, {
    'sequence_features' : fields.List(fields.Nested(sequence_feature), description='Sequence feature representing this particular instance on a genome'),
    'exons' : fields.List(fields.Nested(exon), description='All exons used in this transcript'),
    'cds' : fields.List(fields.Nested(cds), description='All cds used in this transcript'),
    'genes': fields.List(fields.Nested(entity_reference), description='References to any gene objects that have this transcript. This may not be populated if this is contained in a gene object'),
})

gene = api.inherit('Gene', bio_object, {
    'full_name': fields.String(description='full name, e.g. Synaptosome Associated Protein 29'),
    'systematic_name': fields.String(description='E.g. SPBC428.08c for clr4 in PomBase'),
    'description': fields.String(description='full text description'),
    'summaries' : fields.List(fields.Nested(summary_property_value), description='Attributed textual summaries'),
    'chromosome': fields.Nested(chromosome, description='chromosome on which this gene is located. This may be redundant with information in sequence_feature objects but is included here for convenience'),
    'sequence_features' : fields.List(fields.Nested(sequence_feature), description='Sequence feature representing particular instance on a genome'),
    'transcripts' : fields.List(fields.Nested(transcript), description='All transcripts belonging to this gene'),
    'families' : fields.List(fields.Nested(named_object), description='Families, superfamilies etc to which these gene belongs'),
    'phenotype_associations': fields.List(fields.Nested(association), description='phenotypes associated with alterations of gene'),
    'disease_associations': fields.List(fields.Nested(association), description='diseases associated with alterations of gene'),
    'homology_associations': fields.List(fields.Nested(association), description='orthology and paralogy assocations for this gene'),
    'function_associations': fields.List(fields.Nested(association), description='GO assocations for wild type gene'),
    'pathway_associations': fields.List(fields.Nested(association), description='Assocations to pathways in which this gene is involved, including LEGO models'),
    'genotype_associations': fields.List(fields.Nested(association), description='associations to genotypes in which this gene is altered'),
    'interaction_associations': fields.List(fields.Nested(association), description='associations to genes that interact (may be physical or genetic)'),
    'literature_associations': fields.List(fields.Nested(association), description='publications for this gene'),
    #'genotypes': fields.List(fields.Nested(bio_object), desc='List of references to genotype objects')
})


# in GENO, this corresponds to (genotype OR part-of some genotype)
genotype = api.inherit('Genotype', bio_object, {
    #'genes': fields.List(fields.Nested(bio_object), desc='List of references to gene object'),
    'phenotype_associations': fields.List(fields.Nested(association)),
    'disease_associations': fields.List(fields.Nested(association)),
    'gene_associations': fields.List(fields.Nested(association)),
    'variant_associations': fields.List(fields.Nested(association)),
})

allele = api.inherit('Allele', genotype, {
    'sequence_features' : fields.List(fields.Nested(sequence_feature), description='Sequence feature representing particular instance on a genome'),
})

# molecular entities
molecular_complex = api.inherit('MolecularComplex', bio_object, {
    'genes': fields.List(fields.Nested(gene))
})

substance = api.inherit('Substance', bio_object, {
    'target_associations': fields.List(fields.Nested(association)),
    'inchi': fields.List(fields.String),
    'inchi_key': fields.List(fields.String),
    'smiles': fields.List(fields.String),
})

# phylo
phylogenetic_node = api.inherit('PhylogeneticNode', named_object, {
    'feature': fields.Nested(bio_object),
    'parent_id': fields.String,
    'event': fields.String,
    'branch_length': fields.Float
})
phylogenetic_tree = api.inherit('PhylogeneticTree', named_object, {
})

# clinical
clinical_individual = api.inherit('ClinicalIndividual', named_object, {
})
