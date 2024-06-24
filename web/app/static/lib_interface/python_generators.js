python.pythonGenerator.forBlock['move'] = function(block) {  var dropdown_direction = block.getFieldValue('DIRECTION');
  var value_speed = Blockly.Python.valueToCode(block, 'SPEED', Blockly.Python.ORDER_ATOMIC);
  var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);

  var directionFunction = dropdown_direction === 'FORWARD' ? 'forward' : 'backward';

  if (value_duration) {
    var code = `${directionFunction}(${value_speed}, ${value_duration})\n`;
  } else {
    var code = `${directionFunction}(${value_speed})\n`;
  }

  return code;
};


python.pythonGenerator.forBlock['turn'] = function(block) {  var dropdown_direction = block.getFieldValue('DIRECTION');
  var value_speed = Blockly.Python.valueToCode(block, 'SPEED', Blockly.Python.ORDER_ATOMIC);
  var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);

  var directionFunction = dropdown_direction === 'LEFT' ? 'turn_left' : 'turn_right';

  if (value_duration) {
    var code = `${directionFunction}(${value_speed}, ${value_duration})\n`;
  } else {
    var code = `${directionFunction}(${value_speed})\n`;
  }
  return code;
};

python.pythonGenerator.forBlock['stop_rosa'] = function(block) {
  var code = `stop()\n`;
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
  var code = `active_led('${dropdown_led}', '${dropdown_state}')\n`;
  return code;
};

python.pythonGenerator.forBlock['buzzer'] = function(block) {
  var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);
  var code;
  if (value_duration) {
      code = `active_buzz(${value_duration})\n`;
  } else {
      code = `active_buzz()\n`;
  }
  return code;
};


python.pythonGenerator.forBlock['distance_sensor'] = function(block) {
  var code = `get_distance()`
  return code;
};


python.pythonGenerator.forBlock['ground_sensor'] = function(block) {
  var code = `get_ground_distance()`
  return code;
};

