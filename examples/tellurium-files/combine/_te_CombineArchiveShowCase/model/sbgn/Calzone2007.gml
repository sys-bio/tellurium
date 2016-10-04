# generated with VANTED V2.1.0 at Thu Jun 11 15:48:43 BST 2015
graph [
  background_coloring "true"
  cluster_colors "255,204,204,255:0,0,0,255;204,255,255,255:0,0,0,255"
  clusterbackground_fill_outer_region "false"
  clusterbackground_grid 50.0
  clusterbackground_low_alpha 0.2
  clusterbackground_radius 200.0
  clusterbackground_space_fill "true"
  level 2
  sbgn [
    role "PROCESSDESCRIPTION"
  ]
  sbml [
    model_meta_id "metaid_0000002"
    model_name "Calzone2007_CellCycle"
    model_sbml_id "Model_generated_by_BIOCHAM"
    namespace "xmlns:html=\\\"http://www.w3.org/1999/xhtml\\\" xmlns:jigcell=\\\"http://www.sbml.org/2001/ns/jigcell\\\" xmlns:sbml=\\\"http://www.sbml.org/sbml/level2\\\" xmlns:rdf=\\\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\\\" xmlns:math=\\\"http://www.w3.org/1998/Math/MathML\\\" "
    sbml_meta_id "metaid_0000001"
  ]
  sbml_assignment_rule_1 [
    sbml_assignment_rule_1_assignmnet_variable "CycBT"
    sbml_assignment_rule_1_function "(1-N*E_1)*(MPFc+preMPFc)+N*E_1*(MPFn+preMPFn)"
    sbml_assignment_rule_1_meta_id "metaid_0000081"
  ]
  sbml_assignment_rule_2 [
    sbml_assignment_rule_2_assignmnet_variable "StgPT"
    sbml_assignment_rule_2_function "(1-N*E_1)*StgPc+N*E_1*StgPn"
    sbml_assignment_rule_2_meta_id "metaid_0000083"
  ]
  sbml_assignment_rule_3 [
    sbml_assignment_rule_3_assignmnet_variable "Wee1Pc"
    sbml_assignment_rule_3_function "(Wee1T-N*E_1*(Wee1n+Wee1Pn))/(1-N*E_1)-Wee1c"
    sbml_assignment_rule_3_meta_id "metaid_0000084"
  ]
  sbml_compartment_cytoplasm [
    sbml_compartment_cytoplasm_id "cytoplasm"
    sbml_compartment_cytoplasm_meta_id "metaid_0000141"
    sbml_compartment_cytoplasm_size "1.0"
  ]
  sbml_compartment_nuclei [
    sbml_compartment_nuclei_id "nuclei"
    sbml_compartment_nuclei_meta_id "metaid_0000140"
    sbml_compartment_nuclei_size "1.0"
  ]
  sbml_event_1 [
    sbml_event_1_event_assignment_10_function "StgPn/1.95"
    sbml_event_1_event_assignment_10_meta_id "_296309"
    sbml_event_1_event_assignment_10_variable "StgPn"
    sbml_event_1_event_assignment_11_function "MPFc*(1-N*E_1)/(1-1.95*N*E_1)"
    sbml_event_1_event_assignment_11_meta_id "_296321"
    sbml_event_1_event_assignment_11_variable "MPFc"
    sbml_event_1_event_assignment_1_function "factor_1*N"
    sbml_event_1_event_assignment_1_meta_id "_296201"
    sbml_event_1_event_assignment_1_variable "N"
    sbml_event_1_event_assignment_2_function "MPFn/1.95"
    sbml_event_1_event_assignment_2_meta_id "_296213"
    sbml_event_1_event_assignment_2_variable "MPFn"
    sbml_event_1_event_assignment_3_function "preMPFn/1.95"
    sbml_event_1_event_assignment_3_meta_id "_296225"
    sbml_event_1_event_assignment_3_variable "preMPFn"
    sbml_event_1_event_assignment_4_function "Wee1n/1.95"
    sbml_event_1_event_assignment_4_meta_id "_296237"
    sbml_event_1_event_assignment_4_variable "Wee1n"
    sbml_event_1_event_assignment_5_function "Wee1Pn/1.95"
    sbml_event_1_event_assignment_5_meta_id "_296249"
    sbml_event_1_event_assignment_5_variable "Wee1Pn"
    sbml_event_1_event_assignment_6_function "Wee1c*(1-N*E_1)/(1-1.95*N*E_1)"
    sbml_event_1_event_assignment_6_meta_id "_296261"
    sbml_event_1_event_assignment_6_variable "Wee1c"
    sbml_event_1_event_assignment_7_function "Stgn/1.95"
    sbml_event_1_event_assignment_7_meta_id "_296273"
    sbml_event_1_event_assignment_7_variable "Stgn"
    sbml_event_1_event_assignment_8_function "StgPc*(1-N*E_1)/(1-1.95*N*E_1)"
    sbml_event_1_event_assignment_8_meta_id "_296285"
    sbml_event_1_event_assignment_8_variable "StgPc"
    sbml_event_1_event_assignment_9_function "Stgc*(1-N*E_1)/(1-1.95*N*E_1)"
    sbml_event_1_event_assignment_9_meta_id "_296297"
    sbml_event_1_event_assignment_9_variable "Stgc"
    sbml_event_1_meta_id "metaid_0000139"
    sbml_event_1_trigger_function "FZYa >= kez_1"
  ]
  sbml_parameter_1 [
    sbml_parameter_1_id "ksc"
    sbml_parameter_1_meta_id "metaid_0000010"
    sbml_parameter_1_name "ksc"
    sbml_parameter_1_value 0.01
  ]
  sbml_parameter_10 [
    sbml_parameter_10_id "kwee"
    sbml_parameter_10_meta_id "metaid_0000019"
    sbml_parameter_10_name "kweepp"
    sbml_parameter_10_value 1.0
  ]
  sbml_parameter_11 [
    sbml_parameter_11_id "kstgp"
    sbml_parameter_11_meta_id "metaid_0000020"
    sbml_parameter_11_name "kstgp"
    sbml_parameter_11_value 0.2
  ]
  sbml_parameter_12 [
    sbml_parameter_12_id "kstg"
    sbml_parameter_12_meta_id "metaid_0000021"
    sbml_parameter_12_name "kstgpp"
    sbml_parameter_12_value 2.0
  ]
  sbml_parameter_13 [
    sbml_parameter_13_id "ksstg"
    sbml_parameter_13_meta_id "metaid_0000022"
    sbml_parameter_13_name "ksstg"
    sbml_parameter_13_value 0.0
  ]
  sbml_parameter_14 [
    sbml_parameter_14_id "kdstg"
    sbml_parameter_14_meta_id "metaid_0000023"
    sbml_parameter_14_name "kdstg"
    sbml_parameter_14_value 0.0
  ]
  sbml_parameter_15 [
    sbml_parameter_15_id "kastgp"
    sbml_parameter_15_meta_id "metaid_0000024"
    sbml_parameter_15_name "kastgp"
    sbml_parameter_15_value 0.0
  ]
  sbml_parameter_16 [
    sbml_parameter_16_id "kastg"
    sbml_parameter_16_meta_id "metaid_0000025"
    sbml_parameter_16_name "kastgpp"
    sbml_parameter_16_value 1.0
  ]
  sbml_parameter_17 [
    sbml_parameter_17_id "kistg"
    sbml_parameter_17_meta_id "metaid_0000026"
    sbml_parameter_17_name "kistg"
    sbml_parameter_17_value 0.3
  ]
  sbml_parameter_18 [
    sbml_parameter_18_id "kawee"
    sbml_parameter_18_meta_id "metaid_0000027"
    sbml_parameter_18_name "kawee"
    sbml_parameter_18_value 0.3
  ]
  sbml_parameter_19 [
    sbml_parameter_19_id "kiweep"
    sbml_parameter_19_meta_id "metaid_0000028"
    sbml_parameter_19_name "kiweep"
    sbml_parameter_19_value 0.01
  ]
  sbml_parameter_2 [
    sbml_parameter_2_id "kdc"
    sbml_parameter_2_meta_id "metaid_0000011"
    sbml_parameter_2_name "kdcp"
    sbml_parameter_2_value 0.01
  ]
  sbml_parameter_20 [
    sbml_parameter_20_id "kiwee"
    sbml_parameter_20_meta_id "metaid_0000029"
    sbml_parameter_20_name "kiweepp"
    sbml_parameter_20_value 1.0
  ]
  sbml_parameter_21 [
    sbml_parameter_21_id "kt"
    sbml_parameter_21_meta_id "metaid_0000030"
    sbml_parameter_21_name "kin"
    sbml_parameter_21_value 0.15
  ]
  sbml_parameter_22 [
    sbml_parameter_22_id "Jaie"
    sbml_parameter_22_meta_id "metaid_0000031"
    sbml_parameter_22_name "Jaie"
    sbml_parameter_22_value 0.01
  ]
  sbml_parameter_23 [
    sbml_parameter_23_id "Jiie"
    sbml_parameter_23_meta_id "metaid_0000032"
    sbml_parameter_23_name "Jiie"
    sbml_parameter_23_value 0.01
  ]
  sbml_parameter_24 [
    sbml_parameter_24_id "Jafzy"
    sbml_parameter_24_meta_id "metaid_0000033"
    sbml_parameter_24_name "Jafzy"
    sbml_parameter_24_value 0.01
  ]
  sbml_parameter_25 [
    sbml_parameter_25_id "Jifzy"
    sbml_parameter_25_meta_id "metaid_0000034"
    sbml_parameter_25_name "Jifzy"
    sbml_parameter_25_value 0.01
  ]
  sbml_parameter_26 [
    sbml_parameter_26_id "Jastg"
    sbml_parameter_26_meta_id "metaid_0000035"
    sbml_parameter_26_name "Jastg"
    sbml_parameter_26_value 0.05
  ]
  sbml_parameter_27 [
    sbml_parameter_27_id "Jistg"
    sbml_parameter_27_meta_id "metaid_0000036"
    sbml_parameter_27_name "Jistg"
    sbml_parameter_27_value 0.05
  ]
  sbml_parameter_28 [
    sbml_parameter_28_id "Jawee"
    sbml_parameter_28_meta_id "metaid_0000037"
    sbml_parameter_28_name "Jawee"
    sbml_parameter_28_value 0.05
  ]
  sbml_parameter_29 [
    sbml_parameter_29_id "Jiwee"
    sbml_parameter_29_meta_id "metaid_0000038"
    sbml_parameter_29_name "Jiwee"
    sbml_parameter_29_value 0.05
  ]
  sbml_parameter_3 [
    sbml_parameter_3_id "kdnp"
    sbml_parameter_3_meta_id "metaid_0000012"
    sbml_parameter_3_name "kdnp"
    sbml_parameter_3_value 0.01
  ]
  sbml_parameter_30 [
    sbml_parameter_30_id "Jm"
    sbml_parameter_30_meta_id "metaid_0000039"
    sbml_parameter_30_name "Jm"
    sbml_parameter_30_value 0.05
  ]
  sbml_parameter_31 [
    sbml_parameter_31_id "kdmp"
    sbml_parameter_31_meta_id "metaid_0000040"
    sbml_parameter_31_name "kdmp"
    sbml_parameter_31_value 0.002
  ]
  sbml_parameter_32 [
    sbml_parameter_32_id "kdm"
    sbml_parameter_32_meta_id "metaid_0000041"
    sbml_parameter_32_name "kdmpp"
    sbml_parameter_32_value 0.2
  ]
  sbml_parameter_33 [
    sbml_parameter_33_id "koutw_1"
    sbml_parameter_33_meta_id "metaid_0000043"
    sbml_parameter_33_name "koutw"
    sbml_parameter_33_value 0.01
  ]
  sbml_parameter_34 [
    sbml_parameter_34_id "kinw_1"
    sbml_parameter_34_meta_id "metaid_0000044"
    sbml_parameter_34_name "kinw"
    sbml_parameter_34_value 0.04
  ]
  sbml_parameter_35 [
    sbml_parameter_35_id "kouts_1"
    sbml_parameter_35_meta_id "metaid_0000045"
    sbml_parameter_35_name "kouts"
    sbml_parameter_35_value 0.02
  ]
  sbml_parameter_36 [
    sbml_parameter_36_id "kins_1"
    sbml_parameter_36_meta_id "metaid_0000046"
    sbml_parameter_36_name "kins"
    sbml_parameter_36_value 0.08
  ]
  sbml_parameter_37 [
    sbml_parameter_37_id "kez_1"
    sbml_parameter_37_meta_id "metaid_0000048"
    sbml_parameter_37_name "kez"
    sbml_parameter_37_value 0.5
  ]
  sbml_parameter_38 [
    sbml_parameter_38_id "factor_1"
    sbml_parameter_38_meta_id "metaid_0000049"
    sbml_parameter_38_name "factor"
    sbml_parameter_38_value 1.95
  ]
  sbml_parameter_39 [
    sbml_parameter_39_id "E_1"
    sbml_parameter_39_meta_id "metaid_0000050"
    sbml_parameter_39_name "E"
    sbml_parameter_39_value 7.0E-5
  ]
  sbml_parameter_4 [
    sbml_parameter_4_id "kdn"
    sbml_parameter_4_meta_id "metaid_0000013"
    sbml_parameter_4_name "kdnpp"
    sbml_parameter_4_value 1.5
  ]
  sbml_parameter_40 [
    sbml_parameter_40_id "ksxp_1"
    sbml_parameter_40_meta_id "metaid_0000051"
    sbml_parameter_40_name "ksxp"
    sbml_parameter_40_value 0.001
  ]
  sbml_parameter_41 [
    sbml_parameter_41_id "ksxm_1"
    sbml_parameter_41_meta_id "metaid_0000052"
    sbml_parameter_41_name "ksxm"
    sbml_parameter_41_value 5.0E-4
  ]
  sbml_parameter_42 [
    sbml_parameter_42_id "kout_1"
    sbml_parameter_42_meta_id "metaid_0000053"
    sbml_parameter_42_name "kout"
    sbml_parameter_42_value 0.0
  ]
  sbml_parameter_43 [
    sbml_parameter_43_constant "false"
    sbml_parameter_43_id "CycBT"
    sbml_parameter_43_meta_id "metaid_0000142"
  ]
  sbml_parameter_44 [
    sbml_parameter_44_id "StringT"
    sbml_parameter_44_meta_id "metaid_0000143"
    sbml_parameter_44_value 0.8
  ]
  sbml_parameter_45 [
    sbml_parameter_45_id "Wee1T"
    sbml_parameter_45_meta_id "metaid_0000144"
    sbml_parameter_45_value 0.8
  ]
  sbml_parameter_46 [
    sbml_parameter_46_constant "false"
    sbml_parameter_46_id "StgPT"
    sbml_parameter_46_meta_id "metaid_0000145"
    sbml_parameter_46_value 0.0
  ]
  sbml_parameter_5 [
    sbml_parameter_5_id "kaie"
    sbml_parameter_5_meta_id "metaid_0000014"
    sbml_parameter_5_name "kaie"
    sbml_parameter_5_value 1.0
  ]
  sbml_parameter_6 [
    sbml_parameter_6_id "kiie"
    sbml_parameter_6_meta_id "metaid_0000015"
    sbml_parameter_6_name "kiie"
    sbml_parameter_6_value 0.4
  ]
  sbml_parameter_7 [
    sbml_parameter_7_id "kafzy"
    sbml_parameter_7_meta_id "metaid_0000016"
    sbml_parameter_7_name "kafzy"
    sbml_parameter_7_value 1.0
  ]
  sbml_parameter_8 [
    sbml_parameter_8_id "kifzy"
    sbml_parameter_8_meta_id "metaid_0000017"
    sbml_parameter_8_name "kifzy"
    sbml_parameter_8_value 0.2
  ]
  sbml_parameter_9 [
    sbml_parameter_9_id "kweep"
    sbml_parameter_9_meta_id "metaid_0000018"
    sbml_parameter_9_name "kweep"
    sbml_parameter_9_value 0.005
  ]
  sbml_unit_definition_1 [
    sbml_unit_definition_1_id "time_1"
    sbml_unit_definition_1_meta_id "metaid_0000008"
    sbml_unit_definition_1_name "min"
    sbml_unit_definition_1_sub_unit_1_ "(60.0 * 10^0 * second)^1.0"
    sbml_unit_definition_1_sub_unit_1_meta_id "_294219"
    sbml_unit_definition_1unit "(60.0 * 10^0 * second)^1.0"
  ]
  directed 1
  node [
    id 1
    zlevel -1

    cluster [
      cluster "cytoplasm"
    ]
    graphics [
      x 236.66666666666669
      y 840.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ 29.63794274455986
    ]
    label "MPFc"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "MPFc"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "cytoplasm"
      initial_concentration 1.0
      sbmlRole "species"
      species_id "MPFc"
      species_meta_id "metaid_0000055"
    ]
  ]
  node [
    id 2
    zlevel -1

    cluster [
      cluster "cytoplasm"
    ]
    graphics [
      x 387.5
      y 1130.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ -202.3939677700816
    ]
    label "preMPFc"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "preMPFc"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "cytoplasm"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "preMPFc"
      species_meta_id "metaid_0000056"
    ]
  ]
  node [
    id 3
    zlevel -1

    cluster [
      cluster "cytoplasm"
    ]
    graphics [
      x 701.6666666666666
      y 1440.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ -157.53198652146483
    ]
    label "StgPc"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "StgPc"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "cytoplasm"
      initial_concentration 0.8
      sbmlRole "species"
      species_id "StgPc"
      species_meta_id "metaid_0000057"
    ]
  ]
  node [
    id 4
    zlevel -1

    cluster [
      cluster "cytoplasm"
    ]
    graphics [
      x 387.5
      y 310.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ -33.19014251860466
    ]
    label "Wee1c"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "Wee1c"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "cytoplasm"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "Wee1c"
      species_meta_id "metaid_0000058"
    ]
  ]
  node [
    id 5
    zlevel -1

    cluster [
      cluster "cytoplasm"
    ]
    graphics [
      x 701.6666666666666
      y 310.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ 105.933346275102
    ]
    label "Wee1Pc"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "Wee1Pc"
      type "text"
    ]
    sbml [
      boundary_condition "true"
      compartment "cytoplasm"
      initial_concentration 0.8
      sbmlRole "species"
      species_id "Wee1Pc"
      species_meta_id "metaid_0000059"
    ]
  ]
  node [
    id 6
    zlevel -1

    cluster [
      cluster "cytoplasm"
    ]
    graphics [
      x 1200.0
      y 1410.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ -38.688131144693465
    ]
    label "Stgm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "Stgm"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "cytoplasm"
      initial_concentration 1.0
      sbmlRole "species"
      species_id "Stgm"
      species_meta_id "metaid_0000060"
    ]
  ]
  node [
    id 7
    zlevel -1

    cluster [
      cluster "cytoplasm"
    ]
    graphics [
      x 1201.25
      y 1190.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ -87.05774256453667
    ]
    label "Xp"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "Xp"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "cytoplasm"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "Xp"
      species_meta_id "metaid_0000061"
    ]
  ]
  node [
    id 8
    zlevel -1

    cluster [
      cluster "cytoplasm"
    ]
    graphics [
      x 1201.25
      y 1670.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ -12.51563926055654
    ]
    label "Stgc"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "Stgc"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "cytoplasm"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "Stgc"
      species_meta_id "metaid_0000062"
    ]
  ]
  node [
    id 9
    zlevel -1

    cluster [
      cluster "cytoplasm"
    ]
    graphics [
      x 1200.0
      y 1010.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ -82.2026480699504
    ]
    label "Xm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "Xm"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "cytoplasm"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "Xm"
      species_meta_id "metaid_0000063"
    ]
  ]
  node [
    id 10
    zlevel -1

    cluster [
      cluster "nuclei"
    ]
    graphics [
      x 1170.0
      y 460.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ 89.09462249406351
    ]
    label "MPFn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "MPFn"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "nuclei"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "MPFn"
      species_meta_id "metaid_0000064"
    ]
  ]
  node [
    id 11
    zlevel -1

    cluster [
      cluster "nuclei"
    ]
    graphics [
      x 1280.0
      y 750.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ -105.77445626449577
    ]
    label "preMPFn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "preMPFn"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "nuclei"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "preMPFn"
      species_meta_id "metaid_0000065"
    ]
  ]
  node [
    id 12
    zlevel -1

    cluster [
      cluster "nuclei"
    ]
    graphics [
      x 1000.0
      y 320.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ 198.56315529024684
    ]
    label "Wee1Pn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "Wee1Pn"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "nuclei"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "Wee1Pn"
      species_meta_id "metaid_0000066"
    ]
  ]
  node [
    id 13
    zlevel -1

    cluster [
      cluster "nuclei"
    ]
    graphics [
      x 1060.0
      y 160.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ 53.049633803342154
    ]
    label "Wee1n"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "Wee1n"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "nuclei"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "Wee1n"
      species_meta_id "metaid_0000067"
    ]
  ]
  node [
    id 14
    zlevel -1

    cluster [
      cluster "nuclei"
    ]
    graphics [
      x 1980.0
      y 710.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ -64.49024808839293
    ]
    label "StgPn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "StgPn"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "nuclei"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "StgPn"
      species_meta_id "metaid_0000068"
    ]
  ]
  node [
    id 15
    zlevel -1

    cluster [
      cluster "nuclei"
    ]
    graphics [
      x 1520.0
      y 770.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ 82.94740557037673
    ]
    label "Stgn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "Stgn"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "nuclei"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "Stgn"
      species_meta_id "metaid_0000069"
    ]
  ]
  node [
    id 16
    zlevel -1

    cluster [
      cluster "nuclei"
    ]
    graphics [
      x 1610.0
      y 410.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ 11.94038636433959
    ]
    label "FZYa"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "FZYa"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "nuclei"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "FZYa"
      species_meta_id "metaid_0000070"
    ]
  ]
  node [
    id 17
    zlevel -1

    cluster [
      cluster "nuclei"
    ]
    graphics [
      x 1440.0
      y 300.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ 214.54715439624238
    ]
    label "IEa_1"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "IEa_1"
      type "text"
    ]
    sbml [
      boundary_condition "false"
      compartment "nuclei"
      initial_concentration 0.0
      sbmlRole "species"
      species_id "IEa_1"
      species_meta_id "metaid_0000072"
    ]
  ]
  node [
    id 18
    zlevel -1

    cluster [
      cluster "nuclei"
    ]
    graphics [
      x 930.0
      y 700.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "oval"
      z_ -37.929028055020005
    ]
    label "N"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "N"
      type "text"
    ]
  ]
  node [
    id 19
    zlevel -1

    graphics [
      x 236.66666666666669
      y 620.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 160.3323647878808
    ]
    label "Synthesis of MPFc"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_1"
      type "text"
    ]
    sbml [
      reaction_id "R_1"
      reaction_meta_id "metaid_0000085"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "ksc*cytoplasm"
      kinetic_law_meta_id "_294243"
    ]
  ]
  node [
    id 20
    zlevel -1

    graphics [
      x 387.5
      y 1250.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -126.68840772735383
    ]
    label "Activation of MPFc"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_2"
      type "text"
    ]
    sbml [
      reaction_id "R_2"
      reaction_meta_id "metaid_0000086"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*(kstgp+kstg*StgPc)*preMPFc"
      kinetic_law_meta_id "_294291"
    ]
  ]
  node [
    id 21
    zlevel -1

    graphics [
      x 387.5
      y 940.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -81.94239275405987
    ]
    label "Inactivation of MPFc"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_3"
      type "text"
    ]
    sbml [
      reaction_id "R_3"
      reaction_meta_id "metaid_0000087"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*(kweep+kwee*Wee1c)*MPFc"
      kinetic_law_meta_id "_294339"
    ]
  ]
  node [
    id 22
    zlevel -1

    graphics [
      x 500.0
      y 1190.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -329.6959808438372
    ]
    label "Degradation of cyclin"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_6"
      type "text"
    ]
    sbml [
      reaction_id "R_6"
      reaction_meta_id "metaid_0000088"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kdc*preMPFc"
      kinetic_law_meta_id "_294363"
    ]
  ]
  node [
    id 23
    zlevel -1

    graphics [
      x 150.0
      y 770.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 150.81673387876907
    ]
    label "degradation of cyclin"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_7"
      type "text"
    ]
    sbml [
      reaction_id "R_7"
      reaction_meta_id "metaid_0000089"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kdc*MPFc"
      kinetic_law_meta_id "_294387"
    ]
  ]
  node [
    id 24
    zlevel -1

    graphics [
      x 470.0
      y 560.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 37.266115586449175
    ]
    label "Inactivation of Wee1c"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_8"
      type "text"
    ]
    sbml [
      reaction_id "R_8"
      reaction_meta_id "metaid_0000090"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*(kiweep+kiwee*MPFc)*Wee1c/(Jiwee+Wee1c)"
      kinetic_law_meta_id "_294435"
    ]
  ]
  node [
    id 25
    zlevel -1

    graphics [
      x 550.0
      y 350.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 24.91181775770224
    ]
    label "Activation of Wee1c"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_9"
      type "text"
    ]
    sbml [
      reaction_id "R_9"
      reaction_meta_id "metaid_0000091"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kawee*Wee1Pc/(Jawee+Wee1Pc)"
      kinetic_law_meta_id "_294485"
    ]
  ]
  node [
    id 26
    zlevel -1

    graphics [
      x 1201.25
      y 1320.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -62.25022166901892
    ]
    label "mRNA of Stg"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_10"
      type "text"
    ]
    sbml [
      reaction_id "R_10"
      reaction_meta_id "metaid_0000092"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*(kdmp*Stgm/(Jm+Stgm)+kdm*Xp*Stgm)"
      kinetic_law_meta_id "_294522"
    ]
  ]
  node [
    id 27
    zlevel -1

    graphics [
      x 1201.25
      y 1510.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -23.63545025446864
    ]
    label "Synthesis of Stg"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_12"
      type "text"
    ]
    sbml [
      reaction_id "R_12"
      reaction_meta_id "metaid_0000093"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*ksstg*Stgm"
      kinetic_law_meta_id "_294558"
    ]
  ]
  node [
    id 28
    zlevel -1

    graphics [
      x 236.66666666666669
      y 1550.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -42.12922571420663
    ]
    label "activation of Stgc"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_13"
      type "text"
    ]
    sbml [
      reaction_id "R_13"
      reaction_meta_id "metaid_0000094"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*(kastgp+kastg*MPFc)*Stgc/(Jastg+Stgc)"
      kinetic_law_meta_id "_294606"
    ]
  ]
  node [
    id 29
    zlevel -1

    graphics [
      x 930.0
      y 1550.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -131.72721598234827
    ]
    label "inactivation of Stgc"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_14"
      type "text"
    ]
    sbml [
      reaction_id "R_14"
      reaction_meta_id "metaid_0000095"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kistg*StgPc/(Jistg+StgPc)"
      kinetic_law_meta_id "_294642"
    ]
  ]
  node [
    id 30
    zlevel -1

    graphics [
      x 1390.0
      y 1670.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 8.247442012326546
    ]
    label "degradation of Stgc"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_15"
      type "text"
    ]
    sbml [
      reaction_id "R_15"
      reaction_meta_id "metaid_0000096"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kdstg*Stgc"
      kinetic_law_meta_id "_294666"
    ]
  ]
  node [
    id 31
    zlevel -1

    graphics [
      x 701.6666666666666
      y 1550.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -274.85696750760826
    ]
    label "degradation of active Stgc"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_16"
      type "text"
    ]
    sbml [
      reaction_id "R_16"
      reaction_meta_id "metaid_0000097"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kdstg*StgPc"
      kinetic_law_meta_id "_294690"
    ]
  ]
  node [
    id 32
    zlevel -1

    graphics [
      x 701.6666666666666
      y 790.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 46.61841269056726
    ]
    label "export of MPF from cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_19"
      type "text"
    ]
    sbml [
      reaction_id "R_19"
      reaction_meta_id "metaid_0000098"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kt*MPFc*E_1*N/(1-N*E_1)"
      kinetic_law_meta_id "_294726"
    ]
  ]
  node [
    id 33
    zlevel -1

    graphics [
      x 701.6666666666666
      y 730.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 29.23727885880077
    ]
    label "import of MPF into cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "importofMPFintocytoplasm_1"
      type "text"
    ]
    sbml [
      reaction_id "importofMPFintocytoplasm_1"
      reaction_meta_id "metaid_0000099"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kout_1*MPFn*E_1*N/(1-N*E_1)"
      kinetic_law_meta_id "_294774"
    ]
  ]
  node [
    id 34
    zlevel -1

    graphics [
      x 701.6666666666666
      y 640.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 110.64732961672355
    ]
    label "import of MPF into nucleus"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "_16"
      type "text"
    ]
    sbml [
      reaction_id "_16"
      reaction_meta_id "metaid_0000100"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kt*MPFc"
      kinetic_law_meta_id "_294810"
    ]
  ]
  node [
    id 35
    zlevel -1

    graphics [
      x 1230.0
      y 590.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 210.29004257021427
    ]
    label "export of MPF from nucleus"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "exportofMPFfromnucleus_1"
      type "text"
    ]
    sbml [
      reaction_id "exportofMPFfromnucleus_1"
      reaction_meta_id "metaid_0000101"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kout_1*MPFn"
      kinetic_law_meta_id "_294836"
    ]
  ]
  node [
    id 36
    zlevel -1

    graphics [
      x 920.0
      y 1130.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -102.8668997100788
    ]
    label "import of preMPF into cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "importofpreMPFintocytoplaslm_1"
      type "text"
    ]
    sbml [
      reaction_id "importofpreMPFintocytoplaslm_1"
      reaction_meta_id "metaid_0000102"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kout_1*preMPFn*N*E_1/(1-N*E_1)"
      kinetic_law_meta_id "_294885"
    ]
  ]
  node [
    id 37
    zlevel -1

    graphics [
      x 701.6666666666666
      y 900.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -177.4939844135988
    ]
    label "export of preMPF from cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_20"
      type "text"
    ]
    sbml [
      reaction_id "R_20"
      reaction_meta_id "metaid_0000103"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kt*preMPFc*E_1*N/(1-N*E_1)"
      kinetic_law_meta_id "_294922"
    ]
  ]
  node [
    id 38
    zlevel -1

    graphics [
      x 850.0
      y 1010.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -212.73912472229134
    ]
    label "import of preMPF into nucleus"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "_18"
      type "text"
    ]
    sbml [
      reaction_id "_18"
      reaction_meta_id "metaid_0000104"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kt*preMPFc"
      kinetic_law_meta_id "_294959"
    ]
  ]
  node [
    id 39
    zlevel -1

    graphics [
      x 1110.0
      y 700.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -201.30589157083853
    ]
    label "export of preMPFn from nucleus"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "exportofpreMPFnfromnucleus_1"
      type "text"
    ]
    sbml [
      reaction_id "exportofpreMPFnfromnucleus_1"
      reaction_meta_id "metaid_0000105"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kout_1*preMPFn"
      kinetic_law_meta_id "_294985"
    ]
  ]
  node [
    id 40
    zlevel -1

    graphics [
      x 900.0
      y 270.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 313.8117302501434
    ]
    label "export of Wee1P from nucleus"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_21"
      type "text"
    ]
    sbml [
      reaction_id "R_21"
      reaction_meta_id "metaid_0000106"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*koutw_1*Wee1Pn"
      kinetic_law_meta_id "_295011"
    ]
  ]
  node [
    id 41
    zlevel -1

    graphics [
      x 940.0
      y 470.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 106.76275978843275
    ]
    label "import of  Wee1P into cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "_182_1"
      type "text"
    ]
    sbml [
      reaction_id "_182_1"
      reaction_meta_id "metaid_0000107"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*koutw_1*Wee1Pn*N*E_1/(1-N*E_1)"
      kinetic_law_meta_id "_295062"
    ]
  ]
  node [
    id 42
    zlevel -1

    graphics [
      x 701.6666666666666
      y 460.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 33.959450831042496
    ]
    label "export of Wee1P from cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_22"
      type "text"
    ]
    sbml [
      reaction_id "R_22"
      reaction_meta_id "metaid_0000108"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kinw_1*Wee1Pc*E_1*N/(1-N*E_1)"
      kinetic_law_meta_id "_295100"
    ]
  ]
  node [
    id 43
    zlevel -1

    graphics [
      x 890.0
      y 360.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 208.52345558992812
    ]
    label "import of Wee1P into nucleus"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "_20"
      type "text"
    ]
    sbml [
      reaction_id "_20"
      reaction_meta_id "metaid_0000109"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kinw_1*Wee1Pc"
      kinetic_law_meta_id "_295139"
    ]
  ]
  node [
    id 44
    zlevel -1

    graphics [
      x 1240.0
      y 170.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 51.543151413341604
    ]
    label "export of Wee1 from nucleus"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_23"
      type "text"
    ]
    sbml [
      reaction_id "R_23"
      reaction_meta_id "metaid_0000110"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*koutw_1*Wee1n"
      kinetic_law_meta_id "_295165"
    ]
  ]
  node [
    id 45
    zlevel -1

    graphics [
      x 701.6666666666666
      y 210.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -2.2292589622330836
    ]
    label "import of Wee1 into cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "_22"
      type "text"
    ]
    sbml [
      reaction_id "_22"
      reaction_meta_id "metaid_0000111"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*koutw_1*Wee1n*N*E_1/(1-N*E_1)"
      kinetic_law_meta_id "_295215"
    ]
  ]
  node [
    id 46
    zlevel -1

    graphics [
      x 701.6666666666666
      y 560.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -82.70165639262514
    ]
    label "export of Wee1c from cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_24"
      type "text"
    ]
    sbml [
      reaction_id "R_24"
      reaction_meta_id "metaid_0000112"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kinw_1*Wee1c*E_1*N/(1-N*E_1)"
      kinetic_law_meta_id "_295251"
    ]
  ]
  node [
    id 47
    zlevel -1

    graphics [
      x 701.6666666666666
      y 130.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -8.29825032431889
    ]
    label "import of Wee1 into nucleus"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "_24"
      type "text"
    ]
    sbml [
      reaction_id "_24"
      reaction_meta_id "metaid_0000113"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kinw_1*Wee1c"
      kinetic_law_meta_id "_295287"
    ]
  ]
  node [
    id 48
    zlevel -1

    graphics [
      x 1960.0
      y 570.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -157.664129143524
    ]
    label "export of StgP from nucleus"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_25"
      type "text"
    ]
    sbml [
      reaction_id "R_25"
      reaction_meta_id "metaid_0000114"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kouts_1*StgPn"
      kinetic_law_meta_id "_295311"
    ]
  ]
  node [
    id 49
    zlevel -1

    graphics [
      x 980.0
      y 1260.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -79.03367686842743
    ]
    label "import of StgP into cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "_26"
      type "text"
    ]
    sbml [
      reaction_id "_26"
      reaction_meta_id "metaid_0000115"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kouts_1*StgPn*E_1*N/(1-N*E_1)"
      kinetic_law_meta_id "_295359"
    ]
  ]
  node [
    id 50
    zlevel -1

    graphics [
      x 701.6666666666666
      y 1210.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -149.72491163044555
    ]
    label "export of StgP from cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_26"
      type "text"
    ]
    sbml [
      reaction_id "R_26"
      reaction_meta_id "metaid_0000116"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kins_1*StgPc*E_1*N/(1-N*E_1)"
      kinetic_law_meta_id "_295395"
    ]
  ]
  node [
    id 51
    zlevel -1

    graphics [
      x 1990.0
      y 920.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -157.46437922232386
    ]
    label "import of StgP into nucleus"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "_28"
      type "text"
    ]
    sbml [
      reaction_id "_28"
      reaction_meta_id "metaid_0000117"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kins_1*StgPc"
      kinetic_law_meta_id "_295431"
    ]
  ]
  node [
    id 52
    zlevel -1

    graphics [
      x 1490.0
      y 710.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 107.38989320139315
    ]
    label "export of Stg from nucleus"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_27"
      type "text"
    ]
    sbml [
      reaction_id "R_27"
      reaction_meta_id "metaid_0000118"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kouts_1*Stgn"
      kinetic_law_meta_id "_295456"
    ]
  ]
  node [
    id 53
    zlevel -1

    graphics [
      x 1470.0
      y 930.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 29.28420674557431
    ]
    label "import of Stg into cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "_30"
      type "text"
    ]
    sbml [
      reaction_id "_30"
      reaction_meta_id "metaid_0000119"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kouts_1*Stgn*E_1*N/(1-N*E_1)"
      kinetic_law_meta_id "_295504"
    ]
  ]
  node [
    id 54
    zlevel -1

    graphics [
      x 1070.0
      y 1550.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -21.61169923215161
    ]
    label "export of Stg from cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_28"
      type "text"
    ]
    sbml [
      reaction_id "R_28"
      reaction_meta_id "metaid_0000120"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kins_1*Stgc*E_1*N/(1-N*E_1)"
      kinetic_law_meta_id "_295540"
    ]
  ]
  node [
    id 55
    zlevel -1

    graphics [
      x 1650.0
      y 810.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 58.32973633365637
    ]
    label "import of Stg into nucleus"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "_32"
      type "text"
    ]
    sbml [
      reaction_id "_32"
      reaction_meta_id "metaid_0000121"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*kins_1*Stgc"
      kinetic_law_meta_id "_295576"
    ]
  ]
  node [
    id 56
    zlevel -1

    graphics [
      x 1380.0
      y 630.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -36.95416150843664
    ]
    label "activation of MPFn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_29"
      type "text"
    ]
    sbml [
      reaction_id "R_29"
      reaction_meta_id "metaid_0000122"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*(kstgp+kstg*StgPn)*preMPFn"
      kinetic_law_meta_id "_295624"
    ]
  ]
  node [
    id 57
    zlevel -1

    graphics [
      x 1130.0
      y 630.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 15.396586184933392
    ]
    label "inactivation of MPFn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_30"
      type "text"
    ]
    sbml [
      reaction_id "R_30"
      reaction_meta_id "metaid_0000123"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*(kweep+kwee*Wee1n)*MPFn"
      kinetic_law_meta_id "_295672"
    ]
  ]
  node [
    id 58
    zlevel -1

    graphics [
      x 1730.0
      y 500.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -75.58873629984541
    ]
    label "degradation of preMPFn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_33"
      type "text"
    ]
    sbml [
      reaction_id "R_33"
      reaction_meta_id "metaid_0000124"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*(kdnp+kdn*FZYa)*preMPFn"
      kinetic_law_meta_id "_295708"
    ]
  ]
  node [
    id 59
    zlevel -1

    graphics [
      x 1570.0
      y 510.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 59.530032695299056
    ]
    label "degradation of MPFn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_34"
      type "text"
    ]
    sbml [
      reaction_id "R_34"
      reaction_meta_id "metaid_0000125"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*(kdnp+kdn*FZYa)*MPFn"
      kinetic_law_meta_id "_295744"
    ]
  ]
  node [
    id 60
    zlevel -1

    graphics [
      x 1500.0
      y 220.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 294.53474329287724
    ]
    label "activation of intermediary enzyme"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_37"
      type "text"
    ]
    sbml [
      reaction_id "R_37"
      reaction_meta_id "metaid_0000126"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kiie*IEa_1/(Jiie+IEa_1)"
      kinetic_law_meta_id "_295768"
    ]
  ]
  node [
    id 61
    zlevel -1

    graphics [
      x 1380.0
      y 370.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 169.8881260369926
    ]
    label "inactivation of intermediary enzyme"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_38"
      type "text"
    ]
    sbml [
      reaction_id "R_38"
      reaction_meta_id "metaid_0000127"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kaie*(1-IEa_1)*MPFn/(Jaie+1-IEa_1)"
      kinetic_law_meta_id "_295804"
    ]
  ]
  node [
    id 62
    zlevel -1

    graphics [
      x 1620.0
      y 320.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 116.01500795572244
    ]
    label "activation of FZY"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_39"
      type "text"
    ]
    sbml [
      reaction_id "R_39"
      reaction_meta_id "metaid_0000128"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kafzy*IEa_1*(1-FZYa)/(Jafzy+1-FZYa)"
      kinetic_law_meta_id "_295840"
    ]
  ]
  node [
    id 63
    zlevel -1

    graphics [
      x 1750.0
      y 310.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -24.72831463760895
    ]
    label "inactivation of FZY"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_40"
      type "text"
    ]
    sbml [
      reaction_id "R_40"
      reaction_meta_id "metaid_0000129"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kifzy*FZYa/(Jifzy+FZYa)"
      kinetic_law_meta_id "_295864"
    ]
  ]
  node [
    id 64
    zlevel -1

    graphics [
      x 1290.0
      y 330.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 143.99518227831155
    ]
    label "inactivation of Wee1n"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_41"
      type "text"
    ]
    sbml [
      reaction_id "R_41"
      reaction_meta_id "metaid_0000130"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*(kiweep+kiwee*MPFn)*Wee1n/(Jiwee+Wee1n)"
      kinetic_law_meta_id "_295912"
    ]
  ]
  node [
    id 65
    zlevel -1

    graphics [
      x 1010.0
      y 220.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 162.7864225290994
    ]
    label "activation of Wee1n"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_42"
      type "text"
    ]
    sbml [
      reaction_id "R_42"
      reaction_meta_id "metaid_0000131"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kawee*Wee1Pn/(Jawee+Wee1Pn)"
      kinetic_law_meta_id "_295948"
    ]
  ]
  node [
    id 66
    zlevel -1

    graphics [
      x 1690.0
      y 590.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 65.56473395586322
    ]
    label "activation of StgPn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_43"
      type "text"
    ]
    sbml [
      reaction_id "R_43"
      reaction_meta_id "metaid_0000132"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*(kastgp+kastg*MPFn)*Stgn/(Jastg+Stgn)"
      kinetic_law_meta_id "_295996"
    ]
  ]
  node [
    id 67
    zlevel -1

    graphics [
      x 1740.0
      y 730.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 10.362696294213352
    ]
    label "inactivation of StgPn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_44"
      type "text"
    ]
    sbml [
      reaction_id "R_44"
      reaction_meta_id "metaid_0000133"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kistg*StgPn/(Jistg+StgPn)"
      kinetic_law_meta_id "_296032"
    ]
  ]
  node [
    id 68
    zlevel -1

    graphics [
      x 1420.0
      y 800.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ 195.33735489012722
    ]
    label "degradation of Stgn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_45"
      type "text"
    ]
    sbml [
      reaction_id "R_45"
      reaction_meta_id "metaid_0000134"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kdstg*Stgn"
      kinetic_law_meta_id "_296056"
    ]
  ]
  node [
    id 69
    zlevel -1

    graphics [
      x 1820.0
      y 580.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -61.95586820460541
    ]
    label "degradation of StgPn"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "R_46"
      type "text"
    ]
    sbml [
      reaction_id "R_46"
      reaction_meta_id "metaid_0000135"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*kdstg*StgPn"
      kinetic_law_meta_id "_296081"
    ]
  ]
  node [
    id 70
    zlevel -1

    graphics [
      x 990.0
      y 670.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -123.56346823927937
    ]
    label "Nuclei"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "Nuclei_1"
      type "text"
    ]
    sbml [
      reaction_id "Nuclei_1"
      reaction_meta_id "metaid_0000136"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "0"
      kinetic_law_meta_id "_296105"
    ]
  ]
  node [
    id 71
    zlevel -1

    graphics [
      x 1200.0
      y 940.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -63.02524915636005
    ]
    label "Zygotic mRNA"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "_50"
      type "text"
    ]
    sbml [
      reaction_id "_50"
      reaction_meta_id "metaid_0000137"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "nuclei*ksxm_1*N"
      kinetic_law_meta_id "_296141"
    ]
  ]
  node [
    id 72
    zlevel -1

    graphics [
      x 1200.0
      y 1090.0
      w 20.0
      h 20.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "rectangle"
      z_ -92.22498365371348
    ]
    label "Zygotic proteins"
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "_51"
      type "text"
    ]
    sbml [
      reaction_id "_51"
      reaction_meta_id "metaid_0000138"
      reaction_non_rdf_annotation "<jigcell:ratelaw jigcell:name=\\\"Local\\\"></jigcell:ratelaw>
                                                                    "
      reversible "false"
      sbmlRole "reaction"
    ]
    sbml_kinetic_law [
      kinetic_law_function "cytoplasm*ksxp_1*Xm"
      kinetic_law_meta_id "_296177"
    ]
  ]
  node [
    id 73
    zlevel -2

    cluster [
      cluster "nuclei"
    ]
    graphics [
      x 1440.0
      y 480.0
      w 1210.0
      h 740.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 8.0
      gradient 0.0
      rounding 60.0
      type "rectangle"
      z_ -37.929028055020005
    ]
    label "nuclei"
    labelgraphics [
      alignment "center"
      anchor "t"
      color "#000000"
      fontName "Arial"
      fontSize 14
      fontStyle "plain"
      type "text"
    ]
    labelgraphics100 [
      alignment "center"
      anchor "hidden"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        localAlign 0.0
        relHor 0.0
        relVert 0.0
      ]
      text "N"
      type "text"
    ]
    sbgn [
      role "COMPARTMENT"
    ]
    sbml [
      boundary_condition "false"
      compartment "nuclei"
      initial_concentration 1.0
      sbmlRole "species"
      species_id "N"
      species_meta_id "metaid_0000074"
    ]
  ]
  node [
    id 74
    zlevel -3

    graphics [
      x 1090.0
      y 890.0
      w 2070.0
      h 1640.0
      fill "#FFFFFF"
      outline "#000000"
      frameThickness 8.0
      gradient 0.0
      rounding 60.0
      type "rectangle"
    ]
    label "cytoplasm"
    labelgraphics [
      alignment "center"
      anchor "t"
      color "#000000"
      fontName "Arial"
      fontSize 14
      fontStyle "plain"
      type "text"
    ]
    sbgn [
      role "COMPARTMENT"
    ]
  ]
  edge [
    id 1
    source 19
    target 1
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_294231"
      sbmlRole "product"
      species "MPFc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 2
    source 2
    target 20
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294255"
      sbmlRole "reactant"
      species "preMPFc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 3
    source 20
    target 1
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_294267"
      sbmlRole "product"
      species "MPFc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 4
    source 3
    target 20
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294279"
      sbmlRole "modifier"
      species "StgPc"
    ]
  ]
  edge [
    id 5
    source 1
    target 21
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294303"
      sbmlRole "reactant"
      species "MPFc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 6
    source 21
    target 2
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_294315"
      sbmlRole "product"
      species "preMPFc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 7
    source 4
    target 21
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294327"
      sbmlRole "modifier"
      species "Wee1c"
    ]
  ]
  edge [
    id 8
    source 2
    target 22
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294351"
      sbmlRole "reactant"
      species "preMPFc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 9
    source 1
    target 23
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294375"
      sbmlRole "reactant"
      species "MPFc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 10
    source 4
    target 24
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294399"
      sbmlRole "reactant"
      species "Wee1c"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 11
    source 24
    target 5
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_294411"
      sbmlRole "product"
      species "Wee1Pc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 12
    source 1
    target 24
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294423"
      sbmlRole "modifier"
      species "MPFc"
    ]
  ]
  edge [
    id 13
    source 5
    target 25
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294447"
      sbmlRole "reactant"
      species "Wee1Pc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 14
    source 25
    target 4
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_294460"
      sbmlRole "product"
      species "Wee1c"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 15
    source 5
    target 25
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294472"
      sbmlRole "modifier"
      species "Wee1Pc"
    ]
  ]
  edge [
    id 16
    source 6
    target 26
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294498"
      sbmlRole "reactant"
      species "Stgm"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 17
    source 7
    target 26
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294510"
      sbmlRole "modifier"
      species "Xp"
    ]
  ]
  edge [
    id 18
    source 27
    target 8
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_294534"
      sbmlRole "product"
      species "Stgc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 19
    source 6
    target 27
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294546"
      sbmlRole "modifier"
      species "Stgm"
    ]
  ]
  edge [
    id 20
    source 8
    target 28
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294570"
      sbmlRole "reactant"
      species "Stgc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 21
    source 28
    target 3
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_294582"
      sbmlRole "product"
      species "StgPc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 22
    source 1
    target 28
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294594"
      sbmlRole "modifier"
      species "MPFc"
    ]
  ]
  edge [
    id 23
    source 3
    target 29
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294618"
      sbmlRole "reactant"
      species "StgPc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 24
    source 29
    target 8
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_294630"
      sbmlRole "product"
      species "Stgc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 25
    source 8
    target 30
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294654"
      sbmlRole "reactant"
      species "Stgc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 26
    source 3
    target 31
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294678"
      sbmlRole "reactant"
      species "StgPc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 27
    source 1
    target 32
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294702"
      sbmlRole "reactant"
      species "MPFc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 28
    source 18
    target 32
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294714"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 29
    source 33
    target 1
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_294738"
      sbmlRole "product"
      species "MPFc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 30
    source 18
    target 33
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294750"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 31
    source 10
    target 33
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294762"
      sbmlRole "modifier"
      species "MPFn"
    ]
  ]
  edge [
    id 32
    source 34
    target 10
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_294786"
      sbmlRole "product"
      species "MPFn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 33
    source 1
    target 34
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294798"
      sbmlRole "modifier"
      species "MPFc"
    ]
  ]
  edge [
    id 34
    source 10
    target 35
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294822"
      sbmlRole "reactant"
      species "MPFn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 35
    source 36
    target 2
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_294849"
      sbmlRole "product"
      species "preMPFc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 36
    source 11
    target 36
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294861"
      sbmlRole "modifier"
      species "preMPFn"
    ]
  ]
  edge [
    id 37
    source 18
    target 36
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294873"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 38
    source 2
    target 37
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294898"
      sbmlRole "reactant"
      species "preMPFc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 39
    source 18
    target 37
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294910"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 40
    source 38
    target 11
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_294935"
      sbmlRole "product"
      species "preMPFn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 41
    source 2
    target 38
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_294947"
      sbmlRole "modifier"
      species "preMPFc"
    ]
  ]
  edge [
    id 42
    source 11
    target 39
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294972"
      sbmlRole "reactant"
      species "preMPFn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 43
    source 12
    target 40
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_294998"
      sbmlRole "reactant"
      species "Wee1Pn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 44
    source 41
    target 5
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295024"
      sbmlRole "product"
      species "Wee1Pc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 45
    source 12
    target 41
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295037"
      sbmlRole "modifier"
      species "Wee1Pn"
    ]
  ]
  edge [
    id 46
    source 18
    target 41
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295050"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 47
    source 5
    target 42
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295075"
      sbmlRole "reactant"
      species "Wee1Pc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 48
    source 18
    target 42
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295087"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 49
    source 43
    target 12
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295113"
      sbmlRole "product"
      species "Wee1Pn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 50
    source 5
    target 43
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295126"
      sbmlRole "modifier"
      species "Wee1Pc"
    ]
  ]
  edge [
    id 51
    source 13
    target 44
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295152"
      sbmlRole "reactant"
      species "Wee1n"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 52
    source 45
    target 4
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295178"
      sbmlRole "product"
      species "Wee1c"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 53
    source 13
    target 45
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295191"
      sbmlRole "modifier"
      species "Wee1n"
    ]
  ]
  edge [
    id 54
    source 18
    target 45
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295203"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 55
    source 4
    target 46
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295227"
      sbmlRole "reactant"
      species "Wee1c"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 56
    source 18
    target 46
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295239"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 57
    source 47
    target 13
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295263"
      sbmlRole "product"
      species "Wee1n"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 58
    source 4
    target 47
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295275"
      sbmlRole "modifier"
      species "Wee1c"
    ]
  ]
  edge [
    id 59
    source 14
    target 48
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295299"
      sbmlRole "reactant"
      species "StgPn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 60
    source 49
    target 3
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295323"
      sbmlRole "product"
      species "StgPc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 61
    source 14
    target 49
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295335"
      sbmlRole "modifier"
      species "StgPn"
    ]
  ]
  edge [
    id 62
    source 18
    target 49
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295347"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 63
    source 3
    target 50
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295371"
      sbmlRole "reactant"
      species "StgPc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 64
    source 18
    target 50
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295383"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 65
    source 51
    target 14
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295407"
      sbmlRole "product"
      species "StgPn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 66
    source 3
    target 51
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295419"
      sbmlRole "modifier"
      species "StgPc"
    ]
  ]
  edge [
    id 67
    source 15
    target 52
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295444"
      sbmlRole "reactant"
      species "Stgn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 68
    source 53
    target 8
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295468"
      sbmlRole "product"
      species "Stgc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 69
    source 15
    target 53
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295480"
      sbmlRole "modifier"
      species "Stgn"
    ]
  ]
  edge [
    id 70
    source 18
    target 53
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295492"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 71
    source 8
    target 54
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295516"
      sbmlRole "reactant"
      species "Stgc"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 72
    source 18
    target 54
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295528"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 73
    source 55
    target 15
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295552"
      sbmlRole "product"
      species "Stgn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 74
    source 8
    target 55
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295564"
      sbmlRole "modifier"
      species "Stgc"
    ]
  ]
  edge [
    id 75
    source 11
    target 56
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295588"
      sbmlRole "reactant"
      species "preMPFn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 76
    source 56
    target 10
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295600"
      sbmlRole "product"
      species "MPFn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 77
    source 14
    target 56
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295612"
      sbmlRole "modifier"
      species "StgPn"
    ]
  ]
  edge [
    id 78
    source 10
    target 57
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295636"
      sbmlRole "reactant"
      species "MPFn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 79
    source 57
    target 11
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295648"
      sbmlRole "product"
      species "preMPFn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 80
    source 13
    target 57
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295660"
      sbmlRole "modifier"
      species "Wee1n"
    ]
  ]
  edge [
    id 81
    source 11
    target 58
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295684"
      sbmlRole "reactant"
      species "preMPFn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 82
    source 16
    target 58
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295696"
      sbmlRole "modifier"
      species "FZYa"
    ]
  ]
  edge [
    id 83
    source 10
    target 59
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295720"
      sbmlRole "reactant"
      species "MPFn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 84
    source 16
    target 59
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295732"
      sbmlRole "modifier"
      species "FZYa"
    ]
  ]
  edge [
    id 85
    source 17
    target 60
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295756"
      sbmlRole "reactant"
      species "IEa_1"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 86
    source 61
    target 17
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295780"
      sbmlRole "product"
      species "IEa_1"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 87
    source 10
    target 61
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295792"
      sbmlRole "modifier"
      species "MPFn"
    ]
  ]
  edge [
    id 88
    source 62
    target 16
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295816"
      sbmlRole "product"
      species "FZYa"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 89
    source 17
    target 62
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295828"
      sbmlRole "modifier"
      species "IEa_1"
    ]
  ]
  edge [
    id 90
    source 16
    target 63
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295852"
      sbmlRole "reactant"
      species "FZYa"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 91
    source 13
    target 64
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295876"
      sbmlRole "reactant"
      species "Wee1n"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 92
    source 64
    target 12
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295888"
      sbmlRole "product"
      species "Wee1Pn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 93
    source 10
    target 64
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295900"
      sbmlRole "modifier"
      species "MPFn"
    ]
  ]
  edge [
    id 94
    source 12
    target 65
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      type "org.graffiti.plugins.views.defaults.PolyLineEdgeShape"
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295924"
      sbmlRole "reactant"
      species "Wee1Pn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 95
    source 65
    target 13
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295936"
      sbmlRole "product"
      species "Wee1n"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 96
    source 15
    target 66
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_295960"
      sbmlRole "reactant"
      species "Stgn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 97
    source 66
    target 14
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_295972"
      sbmlRole "product"
      species "StgPn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 98
    source 10
    target 66
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_295984"
      sbmlRole "modifier"
      species "MPFn"
    ]
  ]
  edge [
    id 99
    source 14
    target 67
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_296008"
      sbmlRole "reactant"
      species "StgPn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 100
    source 67
    target 15
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_296020"
      sbmlRole "product"
      species "Stgn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 101
    source 15
    target 68
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_296044"
      sbmlRole "reactant"
      species "Stgn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 102
    source 14
    target 69
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      reactant_meta_id "_296068"
      sbmlRole "reactant"
      species "StgPn"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 103
    source 70
    target 18
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_296093"
      sbmlRole "product"
      species "N"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 104
    source 71
    target 9
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_296117"
      sbmlRole "product"
      species "Xm"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 105
    source 18
    target 71
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_296129"
      sbmlRole "modifier"
      species "N"
    ]
  ]
  edge [
    id 106
    source 72
    target 7
    graphics [
      fill "#000000"
      outline "#000000"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      rounding 5.0
      thickness 1.0
    ]
    label ""
    labelgraphics [
      alignment "center"
      anchor "c"
      color "#000000"
      fontName "Arial"
      fontSize 12
      fontStyle "plain"
      position [
        absHor 0.0
        absVert 0.0
        alignSegment 0
        relAlign 0.5
      ]
      type "text"
    ]
    sbml [
      product_meta_id "_296153"
      sbmlRole "product"
      species "Xp"
      stoichiometry "1.0"
    ]
  ]
  edge [
    id 107
    source 9
    target 72
    graphics [
      fill "#404040"
      outline "#404040"
      arrow "last"
      frameThickness 1.0
      gradient 0.0
      linemode "5.0 5.0 0.0"
      rounding 5.0
      thickness 1.0
    ]
    sbml [
      modifier_meta_id "_296165"
      sbmlRole "modifier"
      species "Xm"
    ]
  ]
]
