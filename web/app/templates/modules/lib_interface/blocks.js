Blockly.Blocks['move_forward'] = {
  init: function() {
    this.appendValueInput("SPEED")
        .setCheck("Number")
        .appendField("Move forward with speed");
    this.appendValueInput("DURATION")
        .setCheck("Number")
        .appendField("for duration (seconds, optional)");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['move_backward'] = {
  init: function() {
    this.appendValueInput("SPEED")
        .setCheck("Number")
        .appendField("Move backward with speed");
    this.appendValueInput("DURATION")
        .setCheck("Number")
        .appendField("for duration (seconds, optional)");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

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
    this.setColour(120);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};


Blockly.Blocks['turn_left'] = {
  init: function() {
    this.appendValueInput("SPEED")
        .setCheck("Number")
        .appendField("Turn left with speed");
    this.appendValueInput("DURATION")
        .setCheck("Number")
        .appendField("for duration (seconds, optional)");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['turn_right'] = {
  init: function() {
    this.appendValueInput("SPEED")
        .setCheck("Number")
        .appendField("Turn right with speed");
    this.appendValueInput("DURATION")
        .setCheck("Number")
        .appendField("for duration (seconds, optional)");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['stop_robot'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Stop robot");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
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
    this.setColour(120);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};
