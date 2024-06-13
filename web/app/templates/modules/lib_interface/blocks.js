Blockly.Blocks['move'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Move")
        .appendField(new Blockly.FieldDropdown([["forward", "FORWARD"], ["backward", "BACKWARD"]]), "DIRECTION");
    this.appendValueInput("SPEED")
        .setCheck("Number")
        .appendField("with speed");
    this.appendValueInput("DURATION")
        .setCheck("Number")
        .appendField("for duration (seconds, optional)");
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
        .appendField("Turn")
        .appendField(new Blockly.FieldDropdown([["left", "LEFT"], ["right", "RIGHT"]]), "DIRECTION");
    this.appendValueInput("SPEED")
        .setCheck("Number")
        .appendField("with speed");
    this.appendValueInput("DURATION")
        .setCheck("Number")
        .appendField("for duration (seconds, optional)");
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
        .appendField("Sleep for duration (seconds)");
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
          .appendField(new Blockly.FieldDropdown([["gauche", "left"], ["droite", "right"]]), "LED")
          .appendField("état")
          .appendField(new Blockly.FieldDropdown([["allumer", "on"], ["éteindre", "off"]]), "STATE");
      this.setPreviousStatement(true, null);
      this.setNextStatement(true, null);
      this.setColour(30);
      this.setTooltip('');
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
