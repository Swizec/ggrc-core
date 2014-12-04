# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


class RelationshipTypes(object):
  @classmethod
  def types(cls):
    types = {}
    for k, rt in RELATIONSHIP_TYPES.items():
      types[k] = rt.copy()
      types[k].update({ 'relationship_type': k })
    return types

  @classmethod
  def get_type(cls, relationship_type_id):
    return cls.types().get(relationship_type_id, None)

  @classmethod
  def valid_relationship_hash(cls, relationship_type, related_model, endpoint):
    return dict(
      relationship_type=relationship_type,
      related_model=related_model,
      related_model_endpoint=endpoint)

  @classmethod
  def valid_relationship(cls, obj_type, name, rel):
    if 'symmetric' in rel and rel['symmetric']:
      if rel['source_type'] == obj_type and rel['target_type'] == obj_type:
        return cls.valid_relationship_hash(name, obj_type, 'both')
    else:
      if rel['source_type'] == obj_type:
        return cls.valid_relationship_hash(
            name, rel['target_type'], 'destination')
      if rel['target_type'] == obj_type:
        return cls.valid_relationship_hash(
            name, rel['source_type'], 'source')

  @classmethod
  def valid_relationship_helper(cls, obj_type):
    return [
        cls.valid_relationship(obj_type, name, rel)
          for name, rel in cls.types().items()]

  @classmethod
  def valid_relationships(cls, obj_type):
    if not isinstance(obj_type, (str, unicode)):
      if not isinstance(obj_type, type):
        obj_type = obj_type.__class__
      obj_type = obj_type.__name__

    valid_relationships = {}
    for vr in cls.valid_relationship_helper(obj_type):
      if vr and vr['related_model'] not in valid_relationships:
        valid_relationships[vr['related_model']] = vr
    return valid_relationships.values()


RELATIONSHIP_TYPES = {
  'data_asset_has_process': {
    'source_type': "DataAsset",
    'target_type': "Process",
    'forward_phrase': "has",
    'reverse_phrase': "is a process for",
    'forward_description': "This data asset relies upon the following processes.",
    'reverse_description': "This process supports the following data assets."
  },
  'data_asset_relies_upon_data_asset': {
    'source_type': "DataAsset",
    'target_type': "DataAsset",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This data asset relies upon the following data assets.",
    'reverse_description': "This data asset supports the following data assets."
  },
  'data_asset_relies_upon_facility': {
    'source_type': "DataAsset",
    'target_type': "Facility",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This data asset relies upon the following facilities.",
    'reverse_description': "This facility supports the following data assets."
  },
  'data_asset_relies_upon_system': {
    'source_type': "DataAsset",
    'target_type': "System",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This data asset relies upon the following systems.",
    'reverse_description': "This system supports the following data assets."
  },
  'facility_has_process': {
    'source_type': "Facility",
    'target_type': "Process",
    'forward_phrase': "has",
    'reverse_phrase': "is a process for",
    'forward_description': "This facility relies upon the following processes.",
    'reverse_description': "This process supports the following facilities."
  },
  'facility_relies_upon_data_asset': {
    'source_type': "Facility",
    'target_type': "DataAsset",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This facility relies upon the following data assets.",
    'reverse_description': "This data asset supports the following facilities."
  },
  'facility_relies_upon_facility': {
    'source_type': "Facility",
    'target_type': "Facility",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This facility relies upon the following facilities.",
    'reverse_description': "This facility supports the following facilities."
  },
  'facility_relies_upon_system': {
    'source_type': "Facility",
    'target_type': "System",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This facility relies upon the following systems.",
    'reverse_description': "This system supports the following facilities."
  },
  'market_has_process': {
    'source_type': "Market",
    'target_type': "Process",
    'forward_phrase': "has",
    'reverse_phrase': "is a process for",
    'forward_description': "This market relies upon the following processes.",
    'reverse_description': "This process supports the following markets."
  },
  'market_includes_market': {
    'source_type': "Market",
    'target_type': "Market",
    'forward_phrase': "includes",
    'reverse_phrase': "is included in",
    'forward_description': "This market includes the following markets.",
    'reverse_description': "This market is included in the following markets."
  },
  'market_relies_upon_data_asset': {
    'source_type': "Market",
    'target_type': "DataAsset",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This market relies upon the following data assets.",
    'reverse_description': "This data asset supports the following markets."
  },
  'market_relies_upon_facility': {
    'source_type': "Market",
    'target_type': "Facility",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This market relies upon the following facilities.",
    'reverse_description': "This facility supports the following markets."
  },
  'market_relies_upon_system': {
    'source_type': "Market",
    'target_type': "System",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This market relies upon the following systems.",
    'reverse_description': "This system supports the following markets."
  },
  'org_group_has_process': {
    'source_type': "OrgGroup",
    'target_type': "Process",
    'forward_phrase': "has",
    'reverse_phrase': "is a process for",
    'forward_description': "This org group relies upon the following processes.",
    'reverse_description': "This process supports the following org groups."
  },
  'vendor_has_process': {
    'source_type': "Vendor",
    'target_type': "Process",
    'forward_phrase': "has",
    'reverse_phrase': "is a process for",
    'forward_description': "This vendor relies upon the following processes.",
    'reverse_description': "This process supports the following vendors."
  },
  'org_group_is_affiliated_with_org_group': {
    'source_type': "OrgGroup",
    'target_type': "OrgGroup",
    'symmetric': True,
    'forward_phrase': "is affiliated/collaborates with",
    'reverse_phrase': "is affiliated/collaborates with",
    'forward_description': "This org group is affiliated/collaborates with the following org groups.",
    'reverse_description': "This org group is affiliated/collaborates with the following org groups."
  },
  'vendor_is_affiliated_with_vendor': {
    'source_type': "Vendor",
    'target_type': "Vendor",
    'symmetric': True,
    'forward_phrase': "is affiliated/collaborates with",
    'reverse_phrase': "is affiliated/collaborates with",
    'forward_description': "This vendor is affiliated/collaborates with the following vendors.",
    'reverse_description': "This vendor is affiliated/collaborates with the following vendors."
  },
  'org_group_is_responsible_for_data_asset': {
    'source_type': "OrgGroup",
    'target_type': "DataAsset",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This org group is responsible for the following data assets.",
    'reverse_description': "This data asset is overseen by the following org groups."
  },
  'vendor_is_responsible_for_data_asset': {
    'source_type': "Vendor",
    'target_type': "DataAsset",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This vendor is responsible for the following data assets.",
    'reverse_description': "This data asset is overseen by the following vendors."
  },
  'org_group_is_responsible_for_facility': {
    'source_type': "OrgGroup",
    'target_type': "Facility",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This org group is responsible for the following facilities.",
    'reverse_description': "This facility is overseen by the following org groups."
  },
  'vendor_is_responsible_for_facility': {
    'source_type': "Vendor",
    'target_type': "Facility",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This vendor is responsible for the following facilities.",
    'reverse_description': "This facility is overseen by the following vendors."
  },
  'org_group_is_responsible_for_market': {
    'source_type': "OrgGroup",
    'target_type': "Market",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This org group is responsible for the following markets.",
    'reverse_description': "This market is overseen by the following org groups."
  },
  'vendor_is_responsible_for_market': {
    'source_type': "Vendor",
    'target_type': "Market",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This vendor is responsible for the following markets.",
    'reverse_description': "This market is overseen by the following vendors."
  },
  'org_group_is_responsible_for_org_group': {
    'source_type': "OrgGroup",
    'target_type': "OrgGroup",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This org group is responsible for the following org groups.",
    'reverse_description': "This org group is overseen by the following org groups."
  },
  'vendor_is_responsible_for_vendor': {
    'source_type': "Vendor",
    'target_type': "Vendor",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This vendor is responsible for the following vendors.",
    'reverse_description': "This vendor is overseen by the following vendors."
  },
  'org_group_is_responsible_for_process': {
    'source_type': "OrgGroup",
    'target_type': "Process",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This org group is responsible for the following processes.",
    'reverse_description': "This process is overseen by the following org groups."
  },
  'vendor_is_responsible_for_process': {
    'source_type': "Vendor",
    'target_type': "Process",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This vendor is responsible for the following processes.",
    'reverse_description': "This process is overseen by the following vendors."
  },
  'org_group_is_responsible_for_product': {
    'source_type': "OrgGroup",
    'target_type': "Product",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This org group is responsible for the following products.",
    'reverse_description': "This product is overseen by the following org groups."
  },
  'vendor_is_responsible_for_product': {
    'source_type': "Vendor",
    'target_type': "Product",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This vendor is responsible for the following products.",
    'reverse_description': "This product is overseen by the following vendors."
  },
  'org_group_is_responsible_for_project': {
    'source_type': "OrgGroup",
    'target_type': "Project",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This org group is responsible for the following projects.",
    'reverse_description': "This project is overseen by the following org groups."
  },
  'vendor_is_responsible_for_project': {
    'source_type': "Vendor",
    'target_type': "Project",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This vendor is responsible for the following projects.",
    'reverse_description': "This project is overseen by the following vendors."
  },
  'org_group_is_responsible_for_system': {
    'source_type': "OrgGroup",
    'target_type': "System",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This org group is responsible for the following systems.",
    'reverse_description': "This system is overseen by the following org groups."
  },
  'vendor_is_responsible_for_system': {
    'source_type': "Vendor",
    'target_type': "System",
    'forward_phrase': "is responsible for",
    'reverse_phrase': "is overseen by",
    'forward_description': "This vendor is responsible for the following systems.",
    'reverse_description': "This system is overseen by the following vendors."
  },
  'org_group_relies_upon_data_asset': {
    'source_type': "OrgGroup",
    'target_type': "DataAsset",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This org group relies upon the following data assets.",
    'reverse_description': "This data asset supports the following org groups."
  },
  'vendor_relies_upon_data_asset': {
    'source_type': "Vendor",
    'target_type': "DataAsset",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This vendor relies upon the following data assets.",
    'reverse_description': "This data asset supports the following vendors."
  },
  'org_group_relies_upon_facility': {
    'source_type': "OrgGroup",
    'target_type': "Facility",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This org group relies upon the following facilities.",
    'reverse_description': "This facility supports the following org groups."
  },
  'vendor_relies_upon_facility': {
    'source_type': "Vendor",
    'target_type': "Facility",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This vendor relies upon the following facilities.",
    'reverse_description': "This facility supports the following vendors."
  },
  'org_group_relies_upon_org_group': {
    'source_type': "OrgGroup",
    'target_type': "OrgGroup",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This org group relies upon the following org groups.",
    'reverse_description': "This org group supports the following org groups."
  },
  'vendor_relies_upon_org_group': {
    'source_type': "Vendor",
    'target_type': "OrgGroup",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This vendor relies upon the following org groups.",
    'reverse_description': "This org group supports the following vendors."
  },
  'org_group_relies_upon_system': {
    'source_type': "OrgGroup",
    'target_type': "System",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This org group relies upon the following systems.",
    'reverse_description': "This system supports the following org groups."
  },
  'vendor_relies_upon_system': {
    'source_type': "Vendor",
    'target_type': "System",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This vendor relies upon the following systems.",
    'reverse_description': "This system supports the following vendors."
  },
  'product_has_process': {
    'source_type': "Product",
    'target_type': "Process",
    'forward_phrase': "has",
    'reverse_phrase': "is a process for",
    'forward_description': "This product relies upon the following processes.",
    'reverse_description': "This process supports the following products."
  },
  'product_is_affiliated_with_product': {
    'source_type': "Product",
    'target_type': "Product",
    'symmetric': True,
    'forward_phrase': "is affiliated/collaborates with",
    'reverse_phrase': "is affiliated/collaborates with",
    'forward_description': "This product is affiliated/collaborates with the following products.",
    'reverse_description': "This product is affiliated/collaborates with the following products."
  },
  'product_is_sold_into_market': {
    'source_type': "Product",
    'target_type': "Market",
    'forward_phrase': "is sold into",
    'reverse_phrase': "is a market for",
    'forward_description': "This product is sold into the following markets.",
    'reverse_description': "This market is a market for the following products."
  },
  'product_relies_upon_data_asset': {
    'source_type': "Product",
    'target_type': "DataAsset",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This product relies upon the following data assets.",
    'reverse_description': "This data asset supports the following products."
  },
  'product_relies_upon_facility': {
    'source_type': "Product",
    'target_type': "Facility",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This product relies upon the following facilities.",
    'reverse_description': "This facility supports the following products."
  },
  'product_relies_upon_product': {
    'source_type': "Product",
    'target_type': "Product",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This product relies upon the following products.",
    'reverse_description': "This product supports the following products."
  },
  'product_relies_upon_system': {
    'source_type': "Product",
    'target_type': "System",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This product relies upon the following systems.",
    'reverse_description': "This system supports the following products."
  },
  'program_applies_to_data_asset': {
    'source_type': "Program",
    'target_type': "DataAsset",
    'forward_phrase': "applies to",
    'reverse_phrase': "is within scope of",
    'forward_description': "This program applies to the following data assets.",
    'reverse_description': "This data asset is within scope of the following programs."
  },
  'program_applies_to_facility': {
    'source_type': "Program",
    'target_type': "Facility",
    'forward_phrase': "applies to",
    'reverse_phrase': "is within scope of",
    'forward_description': "This program applies to the following facilities.",
    'reverse_description': "This facility is within scope of the following programs."
  },
  'program_applies_to_market': {
    'source_type': "Program",
    'target_type': "Market",
    'forward_phrase': "applies to",
    'reverse_phrase': "is within scope of",
    'forward_description': "This program applies to the following markets.",
    'reverse_description': "This market is within scope of the following programs."
  },
  'program_applies_to_org_group': {
    'source_type': "Program",
    'target_type': "OrgGroup",
    'forward_phrase': "applies to",
    'reverse_phrase': "is within scope of",
    'forward_description': "This program applies to the following org groups.",
    'reverse_description': "This org group is within scope of the following programs."
  },
  'program_applies_to_vendor': {
    'source_type': "Program",
    'target_type': "Vendor",
    'forward_phrase': "applies to",
    'reverse_phrase': "is within scope of",
    'forward_description': "This program applies to the following vendors.",
    'reverse_description': "This vendor is within scope of the following programs."
  },
  'program_applies_to_process': {
    'source_type': "Program",
    'target_type': "Process",
    'forward_phrase': "applies to",
    'reverse_phrase': "is within scope of",
    'forward_description': "This program applies to the following processes.",
    'reverse_description': "This process is within scope of the following programs."
  },
  'program_applies_to_product': {
    'source_type': "Program",
    'target_type': "Product",
    'forward_phrase': "applies to",
    'reverse_phrase': "is within scope of",
    'forward_description': "This program applies to the following products.",
    'reverse_description': "This product is within scope of the following programs."
  },
  'program_applies_to_project': {
    'source_type': "Program",
    'target_type': "Project",
    'forward_phrase': "applies to",
    'reverse_phrase': "is within scope of",
    'forward_description': "This program applies to the following projects.",
    'reverse_description': "This project is within scope of the following programs."
  },
  'program_applies_to_system': {
    'source_type': "Program",
    'target_type': "System",
    'forward_phrase': "applies to",
    'reverse_phrase': "is within scope of",
    'forward_description': "This program applies to the following systems.",
    'reverse_description': "This system is within scope of the following programs."
  },
  'project_has_process': {
    'source_type': "Project",
    'target_type': "Process",
    'forward_phrase': "has",
    'reverse_phrase': "is a process for",
    'forward_description': "This project relies upon the following processes.",
    'reverse_description': "This process supports the following projects."
  },
  'project_relies_upon_data_asset': {
    'source_type': "Project",
    'target_type': "DataAsset",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This project relies upon the following data assets.",
    'reverse_description': "This data asset supports the following projects."
  },
  'project_relies_upon_facility': {
    'source_type': "Project",
    'target_type': "Facility",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This project relies upon the following facilities.",
    'reverse_description': "This facility supports the following projects."
  },
  'project_relies_upon_system': {
    'source_type': "Project",
    'target_type': "System",
    'forward_phrase': "relies upon",
    'reverse_phrase': "supports",
    'forward_description': "This project relies upon the following systems.",
    'reverse_description': "This system supports the following projects."
  },
  'project_targets_data_asset': {
    'source_type': "Project",
    'target_type': "DataAsset",
    'forward_phrase': "targets",
    'reverse_phrase': "is targeted by",
    'forward_description': "This project targets the following data assets.",
    'reverse_description': "This data asset is targeted by the following projects."
  },
  'project_targets_facility': {
    'source_type': "Project",
    'target_type': "Facility",
    'forward_phrase': "targets",
    'reverse_phrase': "is targeted by",
    'forward_description': "This project targets the following facilities.",
    'reverse_description': "This facility is targeted by the following projects."
  },
  'project_targets_market': {
    'source_type': "Project",
    'target_type': "Market",
    'forward_phrase': "targets",
    'reverse_phrase': "is targeted by",
    'forward_description': "This project targets the following markets.",
    'reverse_description': "This market is targeted by the following projects."
  },
  'project_targets_org_group': {
    'source_type': "Project",
    'target_type': "OrgGroup",
    'forward_phrase': "targets",
    'reverse_phrase': "is targeted by",
    'forward_description': "This project targets the following org groups.",
    'reverse_description': "This org group is targeted by the following projects."
  },
  'project_targets_vendor': {
    'source_type': "Project",
    'target_type': "Vendor",
    'forward_phrase': "targets",
    'reverse_phrase': "is targeted by",
    'forward_description': "This project targets the following vendors.",
    'reverse_description': "This vendor is targeted by the following projects."
  },
  'project_targets_product': {
    'source_type': "Project",
    'target_type': "Product",
    'forward_phrase': "targets",
    'reverse_phrase': "is targeted by",
    'forward_description': "This project targets the following products.",
    'reverse_description': "This product is targeted by the following projects."
  },
}

