import React, { Component } from 'react';
import { Panel } from './Panel';
import './index.css';
import { BotList } from './BotList';
import * as $ from "jquery";

window.jQuery = window.$ = $;

var names = ["Delta", "Beta", "Gamma", "Tau", "Epsilon", "Theta", "Omega", "Alpha", "Eta", "Zeta"];

export var IntegertoName = (id) => {
  let y = "";
  do {
    y += names[id % 10] + " "
    id = Math.floor(id / 10)
  } while (id > 0);
  return y;
}

export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      settings: [],
      numbers: [],
      selected: [],
      singleselected: -1,
      defaultsettings: { "k": 3 },
      passedSettings: { "k": 3 },
      type: 0,
      lastId: 0,
    }
  }
  refresh = () => {
    var route = "http://192.168.100.5:9999/proxy/http://192.168.100.5:5000" + '/getbotlist';
    var method = 'POST';
    /*var username = $("#username").val();
    var password = $("#password").val();*/
    var body = {
      //"admin_roll": username,
      //"admin_pass": password
    }
    var request = $.ajax({
      url: route,
      method: method,
      data: body
    });

    request.done((data) => {
      let settings = JSON.parse(data)
      let numbers = Array.apply(null, { length: settings.length }).map(Function.call, Number);
      let selected = new Array(settings.length);
      selected.fill(false, 0, settings.length - 1);
      this.setState({
        settings: settings,
        numbers: numbers,
        selected: selected,
        type: 0,
        lastId: settings[settings.length - 1]['id'],
      })
    });
  }
  modifyBot = (setting) => {
    let numbers = this.state.numbers.slice();
    let settings = this.state.settings.slice();
    if (this.state.type == 1) {
      let mysettings = JSON.parse(setting);
      console.log(settings);
      settings[this.state.singleselected]['settings'] = JSON.parse(setting);
    }
    this.setState({
      numbers: numbers,
      settings: settings,
      type: 0,
      selectedIndex: -1,
    });
  }

  addBot = (name, type, setting, count) => {
    var route = "http://192.168.100.5:9999/proxy/http://192.168.100.5:5000" + '/createbot';
    let lastId = this.state.lastId
    var method = 'POST';
    /*var username = $("#username").val();
    var password = $("#password").val();*/
    if (count == 1) {
      var body = {
        //"admin_roll": username,
        "bot_name": name,
        "bot_type": type,
        "bot_settings": setting,
        //"admin_pass": password
      }
      var request = $.ajax({
        url: route,
        method: method,
        data: body
      });
      console.log(body);
      request.done((data) => {
        this.refresh()
      });
    } else {
      let rangeSettings = JSON.parse(setting);
      console.log(count);
      for (var i = 0; i < count; i++) {
        let currentSettings = {};
        for (var key in rangeSettings) {
          if (Object.prototype.toString.call(rangeSettings[key]) === '[object Array]') {
            let range = (rangeSettings[key][1] - rangeSettings[key][0]);
            currentSettings[key] = Math.floor(rangeSettings[key][0] + range * Math.random())
          } else {
            currentSettings[key] = rangeSettings[key]
          }
        }
        var body = {
          //"admin_roll": username,
          "bot_name": IntegertoName(lastId + i),
          "bot_type": type,
          "bot_settings": JSON.stringify(currentSettings),
          //"admin_pass": password
        }
        var request = $.ajax({
          url: route,
          method: method,
          data: body
        });
        console.log(body);
        request.done((data) => {
        });
      }
    }
  }
  cancel = () => {
    this.setState({
      type: 0,
      passedSettings: this.state.defaultsettings,
    })
  }
  handleSingleSelect = (number) => {
    console.log(number)
    console.log(this.state.settings);
    console.log(this.state.settings[number])
    var x = this.state.settings[number]['settings']
    var selected = this.state.selected;
    for (var i = 0; i < selected.length; i++) {
      selected[i] = false;
    }
    this.setState({
      type: 1,
      passedSettings: x,
      singleselected: number,
      selected: selected,
    })
  }
  selectAll = (selected) => {
    this.setState({
      selected: selected,
      type: 2
    })
  }
  render() {
    return <div className="app">
      <Panel hello="blue"
        modifyBot={this.modifyBot}
        add={this.addBot}
        refresh={this.refresh}
        cancel={this.cancel}
        type={this.state.type}
        selectedIndex={this.state.singleselected}
        selected={this.state.selected}
        setting={this.state.passedSettings}
        allSettings={this.state.settings} />
      <BotList numbers={this.state.numbers}
        settings={this.state.settings}
        selected={this.state.selected}
        selectAll={this.selectAll}
        handleSingleSelect={this.handleSingleSelect}
      />
    </div>
  }
}