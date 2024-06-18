python.pythonGenerator.forBlock['move'] = function(block) {  var dropdown_direction = block.getFieldValue('DIRECTION');
  var value_speed = Blockly.Python.valueToCode(block, 'SPEED', Blockly.Python.ORDER_ATOMIC);
  var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);

  var directionFunction = dropdown_direction === 'FORWARD' ? 'forward' : 'backward';

  if (value_duration) {
    var code = `${directionFunction}(rosa, ${value_speed}, ${value_duration})\n`;
  } else {
    var code = `${directionFunction}(rosa, ${value_speed})\n`;
  }

  return code;
};


python.pythonGenerator.forBlock['turn'] = function(block) {  var dropdown_direction = block.getFieldValue('DIRECTION');
  var value_speed = Blockly.Python.valueToCode(block, 'SPEED', Blockly.Python.ORDER_ATOMIC);
  var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);

  var directionFunction = dropdown_direction === 'LEFT' ? 'turn_left' : 'turn_right';

  if (value_duration) {
    var code = `${directionFunction}(rosa, ${value_speed}, ${value_duration})\n`;
  } else {
    var code = `${directionFunction}(rosa, ${value_speed})\n`;
  }
  return code;
};

python.pythonGenerator.forBlock['stop_rosa'] = function(block) {
  var code = `stop(rosa)\n`;
  return code;
};

python.pythonGenerator.forBlock['sleep'] = function(block) {
  var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);
  var code = `sleep(${value_duration})\n`;
  return code;
};


python.pythonGenerator.forBlock['led'] = function(block) {
  var dropdown_led = block.getFieldValue('LED');
  var dropdown_state = block.getFieldValue('STATE');
  var code = `active_led(rosa, '${dropdown_led}', '${dropdown_state}')\n`;
  return code;
};

python.pythonGenerator.forBlock['buzzer'] = function(block) {
  var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);
  var code;
  if (value_duration) {
      code = `active_buzz(rosa, ${value_duration})\n`;
  } else {
      code = `active_buzz(rosa)\n`;
  }
  return code;
};
