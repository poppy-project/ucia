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

Blockly.Blocks['ground_sensor'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Valeur du capteur de ligne")
        .appendField(new Blockly.FieldDropdown([["gauche", "left"], ["droite", "right"]]), "SENSOR");
    this.setOutput(true, 'Number');
    this.setColour(30);
    this.setTooltip('Mesure la valeur du capteur de sol indiqué');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['distance_sensor'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Valeur du capteur ")
        .appendField(new Blockly.FieldDropdown([["av1", "4"], ["av2", "3"], ["av3", "2"], ["av4", "1"], ["av5", "0"], ["ar1", "5"], ["ar2", "6"]]), "SENSOR");
    this.setOutput(true, 'Number');
    this.setColour(30);
    this.setTooltip('Mesure la distance du capteur de distance indiqué');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['led'] = {
  init: function() {
      this.appendDummyInput()
          .appendField("Contrôler LED")
          .appendField(new Blockly.FieldDropdown([["gauche", "left"], ["droite", "right"], ["toutes", "both"]]), "LED")
          .appendField("couleur")
          .appendField(new Blockly.FieldDropdown([["rouge", "red"], ["vert", "green"], ["bleu", "blue"], ["jaune", "yellow"], ["violet", "purple"], ["cyan", "cyan"], ["blanc", "white"]]), "COLOR");
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


Blockly.Blocks['sound'] = {
  init: function() {
    this.appendValueInput("FREQUENCY")
        .setCheck("Number")
        .appendField("Produire un son à la fréquence");
    this.appendValueInput("DURATION")
        .setCheck("Number")
        .appendField("pendant (seconds)");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(30);
    this.setTooltip('');
    this.setHelpUrl('');
  }
};

Blockly.Blocks['song'] = {
  init: function() {
    this.appendDummyInput()
        .appendField("Jouer la")
        .appendField(new Blockly.FieldDropdown([
          ["mélodie 1", "twinkle_twinkle"],
          ["mélodie 2", "frere_jacques"],
          ["mélodie 3", "mary_had_a_little_lamb"],
          ["mélodie 4", "ode_to_joy"]
        ]), "MELODIE");
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(30);
    this.setTooltip('Joue la mélodie indiquée');
    this.setHelpUrl('');
  }
};
