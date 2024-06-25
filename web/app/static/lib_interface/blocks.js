Blockly.Blocks['move'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Déplacement vers l'")
        .appendField(new Blockly.FieldDropdown([["avant", "FORWARD"], ["arrière", "BACKWARD"]]), "DIRECTION");
    this.appendValueInput("SPEED")
        .setCheck("Number")
        .appendField("à la vitesse (entre 0 et 100)");
    this.appendValueInput("DURATION")
        .setCheck("Number")
        .appendField("attendre pendant (seconds, optionnel)");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(30);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};


Blockly.Blocks['turn'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Tourner vers la")
        .appendField(new Blockly.FieldDropdown([["gauche", "LEFT"], ["droite", "RIGHT"]]), "DIRECTION");
    this.appendValueInput("SPEED")
        .setCheck("Number")
        .appendField("à la vitesse (entre 0 et 100)");
    this.appendValueInput("DURATION")
        .setCheck("Number")
        .appendField("attendre pendant (seconds, optionnel)");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(30);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};


Blockly.Blocks['stop_rosa'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Stop ROSA");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(30);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['sleep'] = {
  init: function() {
    this.appendValueInput("DURATION")
        .setCheck("Number")
        .appendField("Attendre pendant (seconds)");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(30);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['led'] = {
  init: function() {
      this.appendDummyInput()
          .appendField("Contrôler LED")
          .appendField(new Blockly.FieldDropdown([["gauche", "left"], ["droite", "right"], ["toutes", "both"]]), "LED")
          .appendField("couleur")
          .appendField(new Blockly.FieldDropdown([["éteindre", "off"], ["rouge", "red"], ["vert", "green"], ["bleu", "blue"], ["jaune", "yellow"], ["violet", "purple"], ["cyan", "cyan"], ["blanc", "white"]]), "COLOR");
      this.appendValueInput("DURATION")
          .setCheck("Number")
          .appendField("pendant la durée (secondes)");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(30);
      this.setTooltip('');
      this.setHelpUrl('');
  }
};

Blockly.Blocks['ground_sensor'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Distance du capteur")
        .appendField(new Blockly.FieldDropdown([["gauche", "LEFT"], ["droite", "RIGHT"]]), "DIRECTION");
    this.setOutput(true, 'Number');
    this.setColour(30);
    this.setTooltip('Mesure la distance du capteur au sol pour le capteur gauche ou droit');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['buzzer'] = {
  init: function() {
      this.appendDummyInput()
          .appendField("Activer le buzzer");
      this.appendValueInput("DURATION")
          .setCheck("Number")
          .appendField("pendant la durée (secondes, optionnel)");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(30);
      this.setTooltip('');
      this.setHelpUrl('');
  }
};
