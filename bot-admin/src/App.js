import React, { Component } from 'react';
import PNotify from 'pnotify/dist/es/PNotify';
import { Panel } from './Panel';
import './index.css';
import { BotList } from './BotList';
import * as $ from "jquery";

window.jQuery = window.$ = $;
export const BASE_URL = "http://0.0.0.0:5000"
var names = ["Delta", "Beta", "Gamma", "Tau", "Epsilon", "Theta", "Omega", "Alpha", "Eta", "Zeta"];

export var IntegertoName = (id) => {
  let y = "";
  let namesLength = names.length;
  do {
    y += names[id % namesLength] + " "
    id = Math.floor(id / namesLength)
  } while (id > 0);
  return y;
}

export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      settings: [], // array of bots retrieved. 
      numbers: [],
      selected: [],
      singleselected: -1,
      defaultsettings: { "k": 3 },
      passedSettings: { "k": 3 },
      type: 0, // 0 for nothing selected
      lastId: 0,
    }
    this.refresh();
  }
  refresh = () => {
    let route = BASE_URL + '/getbotlist';
    let method = 'GET';
    let request = $.ajax({
      url: route,
      method: method,
      data: {}
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
        lastId: ((settings[settings.length - 1]) ? settings[settings.length - 1]['id'] : 0),
      })
    }).fail((req, textStatus, errorThrown) => {
      PNotify.alert(req.responseText);
    });
  }
  modifyBot = (setting) => {
    let numbers = this.state.numbers.slice();
    let settings = this.state.settings.slice();
    if (this.state.type == 1) {
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
    var route = BASE_URL + '/createbot';
    let lastId = this.state.lastId
    var method = 'POST';
    if (count == 1) {
      var body = {
        "bot_name": name,
        "bot_type": type,
        "bot_settings": setting,
      }
      var request = $.ajax({
        url: route,
        method: method,
        data: body
      });
      request.done((data) => {
        this.refresh()
      });
    } else {
      let rangeSettings = JSON.parse(setting);
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
          "bot_name": IntegertoName(lastId + i+1),
          "bot_type": type,
          "bot_settings": JSON.stringify(currentSettings),
        }
        var request = $.ajax({
          url: route,
          method: method,
          data: body
        });
        let usercount=0;
        request.done((data) => {
          this.refresh();
        });
      }
    }
  }
  cancel = () => {
    let selected = new Array(this.state.settings.length);
      selected.fill(false, 0, this.state.settings.length - 1);
    this.setState({
      selected:selected,
      type: 0,
      passedSettings: this.state.defaultsettings,
    })
  }
  handleSingleSelect = (number) => {
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
      <Panel hello="orange"
        modifyBot={this.modifyBot}
        add={this.addBot}
        refresh={this.refresh}
        cancel={this.cancel}
        type={this.state.type}
        selectedIndex={this.state.singleselected}
        selected={this.state.selected}
        setting={this.state.passedSettings}
        allSettings={this.state.settings}
        botTypes={this.state.bot_types} />
      <BotList numbers={this.state.numbers}
        settings={this.state.settings}
        selected={this.state.selected}
        selectAll={this.selectAll}
        handleSingleSelect={this.handleSingleSelect}
      />
    </div>
  }
}