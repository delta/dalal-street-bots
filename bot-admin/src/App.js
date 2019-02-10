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
			botList: [], // array of bots retrieved. 
			selected: {}, // mapping from botId to state
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
		});
		request.done((data) => {
			let botList = Object.values(JSON.parse(data));
			let selected = {};
			for (const botObjId in botList) {
				let botObj = botList[botObjId];
				selected[botObj['id']] = false;
			}
			this.setState({
				botList: botList,
				selected: selected,
			});
		}).fail((req, textStatus, errorThrown) => {
			PNotify.alert(req.responseText);
		});
	}
	
	// modifyBot is passed like settings which is updated for each bot that was selected
	modifyBot = (newSettings) => {
		let botTypeMapping = {};
		for(let i = 0; i < this.state.botList.length; i++) {
			for(const botObjId in this.state.selected) {
				if (this.state.botList[i]['id'] === parseInt(botObjId, 10) && this.state.selected[botObjId]) {
					botTypeMapping[this.state.botList[i]['type']] = 1;
				}
			}
		}
		let isMoreThanOneClass = Object.keys(botTypeMapping).length > 1;
		if (isMoreThanOneClass) {
			PNotify.alert("Multi Type changes not allowed: " + Object.keys(botTypeMapping).join(", "));
			return;
		}

		let newBotList = this.state.botList.map((botObj) => {
			botObj['settings'] = newSettings;
			return botObj;	
		});
		this.setState({
			botList: newBotList,
		});
	}
	
	// create single or multiple bots
	addBot = (name, botType, setting, count) => {
		let route = BASE_URL + '/createbot';
		let lastId = this.state.lastId
		let method = 'POST';
		if (count === 1) {
			let body = {
				"bot_name": name,
				"bot_type": botType,
				"bot_settings": setting,
			}
			let request = $.ajax({
				url: route,
				method: method,
				data: body
			});
			request.done((data) => {
				this.refresh()
			});
		} else {
			let rangeSettings = JSON.parse(setting);
			for (let i = 0; i < count; i++) {
				let currentSettings = {};
				for (let key in rangeSettings) {
					if (Object.prototype.toString.call(rangeSettings[key]) === '[object Array]') {
						let range = (rangeSettings[key][1] - rangeSettings[key][0]);
						currentSettings[key] = Math.floor(rangeSettings[key][0] + range * Math.random()) // Randomly pick data in given range [x, y]
					} else {
						currentSettings[key] = rangeSettings[key] // If not range, assign exact value
					}
				}
				let body = {
					"bot_name": IntegertoName(lastId + i+1),
					"bot_type": botType,
					"bot_settings": JSON.stringify(currentSettings),
				}
				let request = $.ajax({
					url: route,
					method: method,
					data: body
				});
				request.done((data) => {
					this.refresh();
				});
			}
		}
	}
	
	// Reset everything to the way it was
	cancel = () => {
		let selected = {};
		let botList = this.state.botList;
		for (const botObjId in botList) {
			let botObj = botList[botObjId];
			selected[botObj['id']] = false;
		}
		this.setState({
			selected: selected,
		})
	}
	
	handleSelection = (selectedEles) => {
		var selected = this.state.selected;
		for (const id in selectedEles) {
			const botObjId = selectedEles[id];
			selected[botObjId] = !selected[botObjId];
		}
		this.setState({
			selected: selected,
		})
	}

	togglePaused = (isPaused) => {
		let botList = this.state.botList;
		let valueToSet = isPaused + 0;
		for(let i = 0; i < botList.length; i++) {
			for(const botObjId in this.state.selected) {
				if (botList[i]['id'] === parseInt(botObjId, 10) && this.state.selected[botObjId]) {
					botList[i]['is_paused'] = valueToSet;
				}
			}
		}
		this.setState({
			botList: botList,
		})
	}
	
	render() {
		return <div className="app">
					<Panel color="orange"
						modifyBot={this.modifyBot}
						add={this.addBot}
						refresh={this.refresh}
						cancel={this.cancel}
						selected={this.state.selected}
						botList={this.state.botList}
						togglePaused={this.togglePaused}
					/>
					<BotList numbers={this.state.numbers}
						botList={this.state.botList}
						selected={this.state.selected}
						handleSelection={this.handleSelection}
					/>
				</div>
	}
}