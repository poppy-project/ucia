Blockly.Python['move_forward'] = function(block) {
    var value_speed = Blockly.Python.valueToCode(block, 'SPEED', Blockly.Python.ORDER_ATOMIC);
    var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);
    if (value_duration) {
      var code = `forward(rosa, ${value_speed}, ${value_duration})\n`;
    } else {
      var code = `forward(rosa, ${value_speed})\n`;
    }
    return code;
  };
  
  Blockly.Python['move_backward'] = function(block) {
    var value_speed = Blockly.Python.valueToCode(block, 'SPEED', Blockly.Python.ORDER_ATOMIC);
    var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);
    if (value_duration) {
      var code = `backward(rosa, ${value_speed}, ${value_duration})\n`;
    } else {
      var code = `backward(rosa, ${value_speed})\n`;
    }
    return code;
  };
  
  Blockly.Python['turn_left'] = function(block) {
    var value_speed = Blockly.Python.valueToCode(block, 'SPEED', Blockly.Python.ORDER_ATOMIC);
    var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);
    if (value_duration) {
      var code = `turn_left(rosa, ${value_speed}, ${value_duration})\n`;
    } else {
      var code = `turn_left(rosa, ${value_speed})\n`;
    }
    return code;
  };
  
  Blockly.Python['turn_right'] = function(block) {
    var value_speed = Blockly.Python.valueToCode(block, 'SPEED', Blockly.Python.ORDER_ATOMIC);
    var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);
    if (value_duration) {
      var code = `turn_right(rosa, ${value_speed}, ${value_duration})\n`;
    } else {
      var code = `turn_right(rosa, ${value_speed})\n`;
    }
    return code;
  };
  
  Blockly.Python['stop_robot'] = function(block) {
    var code = 'stop(rosa)\n';
    return code;
  };
  
  Blockly.Python['sleep'] = function(block) {
    var value_duration = Blockly.Python.valueToCode(block, 'DURATION', Blockly.Python.ORDER_ATOMIC);
    var code = `sleep(${value_duration})\n`;
    return code;
  };
  