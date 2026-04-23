# First-Run Bootstrap

This workspace is for autonomous TESDA CBLM generation.

## Output Schema Expectations
Each generated payload should contain the full template-aligned field set below.

### Core Identity Fields
- sector
- qualification_title
- unit_of_competency
- module_title
- next_unit_of_competency
- Module_Descriptor
- Laboratory
- training_materials
- uc_no

### List of Competencies Table
- unit_of_competency_1
- unit_of_competency_2
- unit_of_competency_3
- unit_of_competency_4

- module_title_1
- module_title_2
- module_title_3
- module_title_4

- unit_of_competency_code_1
- unit_of_competency_code_2
- unit_of_competency_code_3
- unit_of_competency_code_4

### Learning Outcomes
- LO_1
- LO_2
- LO_3

### Contents / Topics
- Contents_1_1
- Contents_1_2
- Contents_1_3

- Contents_2_1
- Contents_2_2
- Contents_2_3

- Contents_3_1
- Contents_3_2
- Contents_3_3

### Key Facts and Exercises

#### Learning Outcome 1
- Contents_1_1_Key_Facts
- Contents_1_1_LE_MC
- Contents_1_1_LE_MC_Answer

- Contents_1_2_Key_Facts
- Contents_1_2_LE_MC
- Contents_1_2_LE_MC_Answer

- Contents_1_3_Key_Facts
- Contents_1_3_LE_MC
- Contents_1_3_LE_MC_Answer

#### Learning Outcome 2
- Contents_2_1_Key_Facts
- Contents_2_1_LE_MC
- Contents_2_1_LE_MC_Answer

- Contents_2_2_Key_Facts
- Contents_2_2_LE_MC
- Contents_2_2_LE_MC_Answer

- Contents_2_3_Key_Facts
- Contents_2_3_LE_MC
- Contents_2_3_LE_MC_Answer

#### Learning Outcome 3
- Contents_3_1_Key_Facts
- Contents_3_1_LE_MC
- Contents_3_1_LE_MC_Answer

- Contents_3_2_Key_Facts
- Contents_3_2_LE_MC
- Contents_3_2_LE_MC_Answer

- Contents_3_3_Key_Facts
- Contents_3_3_LE_MC
- Contents_3_3_LE_MC_Answer

### Let’s Apply Fields

#### Learning Outcome 1
- la_1_1_title
- la_1_1_objective
- la_1_1_sup_mat
- la_1_1_equipment_list
- la_1_1_steps_list
- la_1_1_assessmentmethod
- la_1_1_pc1
- la_1_1_pc2
- la_1_1_pc3
- la_1_1_pc4
- la_1_1_pc5

- la_1_2_title
- la_1_2_objective
- la_1_2_sup_mat
- la_1_2_equipment_list
- la_1_2_steps_list
- la_1_2_assessmentmethod
- la_1_2_pc1
- la_1_2_pc2
- la_1_2_pc3
- la_1_2_pc4
- la_1_2_pc5

- la_1_3_title
- la_1_3_objective
- la_1_3_sup_mat
- la_1_3_equipment_list
- la_1_3_steps_list
- la_1_3_assessmentmethod
- la_1_3_pc1
- la_1_3_pc2
- la_1_3_pc3
- la_1_3_pc4
- la_1_3_pc5

#### Learning Outcome 2
- la_2_1_title
- la_2_1_objective
- la_2_1_sup_mat
- la_2_1_equipment_list
- la_2_1_steps_list
- la_2_1_assessmentmethod
- la_2_1_pc1
- la_2_1_pc2
- la_2_1_pc3
- la_2_1_pc4
- la_2_1_pc5

- la_2_2_title
- la_2_2_objective
- la_2_2_sup_mat
- la_2_2_equipment_list
- la_2_2_steps_list
- la_2_2_assessmentmethod
- la_2_2_pc1
- la_2_2_pc2
- la_2_2_pc3
- la_2_2_pc4
- la_2_2_pc5

- la_2_3_title
- la_2_3_objective
- la_2_3_sup_mat
- la_2_3_equipment_list
- la_2_3_steps_list
- la_2_3_assessmentmethod
- la_2_3_pc1
- la_2_3_pc2
- la_2_3_pc3
- la_2_3_pc4
- la_2_3_pc5

#### Learning Outcome 3
- la_3_1_title
- la_3_1_objective
- la_3_1_sup_mat
- la_3_1_equipment_list
- la_3_1_steps_list
- la_3_1_assessmentmethod
- la_3_1_pc1
- la_3_1_pc2
- la_3_1_pc3
- la_3_1_pc4
- la_3_1_pc5

- la_3_2_title
- la_3_2_objective
- la_3_2_sup_mat
- la_3_2_equipment_list
- la_3_2_steps_list
- la_3_2_assessmentmethod
- la_3_2_pc1
- la_3_2_pc2
- la_3_2_pc3
- la_3_2_pc4
- la_3_2_pc5

- la_3_3_title
- la_3_3_objective
- la_3_3_sup_mat
- la_3_3_equipment_list
- la_3_3_steps_list
- la_3_3_assessmentmethod
- la_3_3_pc1
- la_3_3_pc2
- la_3_3_pc3
- la_3_3_pc4
- la_3_3_pc5

## Field Guidance
- `Module_Descriptor` should be a concise TESDA-style summary of the module and its intended competency coverage.
- `Laboratory` should state the actual or best-fit workplace/training location for the module, such as `Computer Laboratory` for ICT-related modules when no specific site is given.
- `training_materials` should be a newline-separated list of materials to display under the TRAINING MATERIALS section of the template.
- `unit_of_competency_code_1` to `unit_of_competency_code_4` should be extracted from the syllabus if present. If unavailable from the syllabus, they MUST be generated using the standard code format.
- `uc_no` must match the index of the unit currently being generated.
- Use exact placeholder names as they appear in the template.
- Every `Contents_X_Y_Key_Facts` field should be at least 600 words, preferably 650-800 words, paragraph-based, TESDA-style, and should include a concept overview, detailed explanation, real-world example, industry/workplace application, and summary/reinforcement.
- `Contents_X_Y_Key_Facts` fields in the same payload must remain materially distinct from one another, stay anchored to the exact content title and subtopics, vary their framing and examples, and avoid generic filler.
