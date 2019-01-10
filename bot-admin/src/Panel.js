import React, { Component } from 'react';
import './index.css'
import $ from 'jquery'
import { BASE_URL } from './App'

var bot_types = {
    'MacdBot': {
        "sleep_duration": 15, // in seconds. THIS SETTING IS REQUIRED
        "buy_limit": 3, // number of companies to buy at a time
        "stocks_per_company":3, // how many stocks per company do you want to buy at a time
        "holding_time": 3, // how many rounds to hold before you sell your stocks off
        "no_of_companies": 10, // number of companies to buy from
        "bot_tag": "unset", // special tags for searching purpose
        "macd_level": 3, // for signal line
        "macd_newer": 5, // the less-lagging EMA value
        "macd_lagger": 7, // the more - lagging EMA value
    },
    'DumbBot': {
        "sleep_duration": 15, // in seconds. THIS SETTING IS REQUIRED
    },
    'OverBoughtOverSoldBot': {
        "sleep_duration": 15, // in seconds. THIS SETTING IS REQUIRED
        "no_of_companies": 10, // number of companies to buy from. Technically should be ALL
        "bot_tag": "unset", // special tags for searching purpose
        "percentage_change": 10, // the sum percentage change before the bot starts acting
        "cut_down_factor": 2, // how much to cut down the current percentage of increase by
    },
    'StockBuyerBot': {
        "sleep_duration": 3, // in seconds. THIS SETTING IS REQUIRED
        "buy_limit": 3, // number of companies to buy at a time
        "stocks_per_company":3, // how many stocks per company do you want to buy at a time
        "holding_time": 5, // how many rounds to hold before you sell your stocks off
        "no_of_companies": 12, // number of companies to buy from
        "bot_tag": "unset", // special tags for searching purpose
    },
    'StockSellerBot': {
        "sleep_duration": 5, // in seconds. THIS SETTING IS REQUIRED
        "buy_limit": 3, // number of companies to buy at a time
        "stocks_per_company":3, // how many stocks per company do you want to buy at a time
        "holding_time": 5, // how many rounds to hold before you sell your stocks off
        "no_of_companies": 12, // number of companies to buy from
        "bot_tag": "unset", // special tags for searching purpose
    },
    'StockchangerBot': {
        "sleep_duration": 15, // in seconds. THIS SETTING IS REQUIRED
        "buy_limit": 3, // number of companies to buy at a time
        "stocks_per_company":1, // how many stocks per company do you want to buy at a time
        "holding_time": 5, // how many rounds to hold before you sell your stocks off
        "no_of_companies": 1, // number of companies to buy from
        "bot_tag": "unset", // special tags for searching purpose
        "impact": 0,
        "stockId":1,
    },
    'EmaBot': {
        "sleep_duration": 5, // in seconds. THIS SETTING IS REQUIRED
        "buy_limit": 3, // number of companies to buy at a time
        "stocks_per_company":3, // how many stocks per company do you want to buy at a time
        "holding_time": 5, // how many rounds to hold before you sell your stocks off
        "no_of_companies": 10, // number of companies to buy from
        "bot_tag": "unset", // special tags for searching purpose
        "k": 5
    },
    'RsiBot': {
        "sleep_duration": 15, // in seconds. THIS SETTING IS REQUIRED
        "buy_limit": 3, // number of companies to buy at a time
        "stocks_per_company":3, // how many stocks per company do you want to buy at a time
        "holding_time": 3, // how many rounds to hold before you sell your stocks off
        "no_of_companies": 10, // number of companies to buy from
        "bot_tag": "unset", // special tags for searching purpose
        "k": 5,
    }
};


export class Panel extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            setting: JSON.stringify(this.props.setting, null, 4),
            name: "",
            type: "",
            logs: "",
            count: 1,
        }
    }
    getLogs = (index) => {
        var route = BASE_URL + '/getlogs';
        var method = 'POST';
        console.log(index);
        console.log(this.props.setting)
        var userId = this.props.allSettings[index]['id']
        var body = {
            "bot_id": userId,
            //"admin_pass": password
        }
        var request = $.ajax({
            url: route,
            method: method,
            data: body
        });

        request.done((data) => {
            console.log("hi")
            console.log(data);
            let x = JSON.parse(data);
            let y = "";
            console.log(x)
            Object.keys(x).map((val) => {
                y += x[val][2] + " : " + x[val][1] + "\n"
            })
            this.setState({
                logs: y
            });
        });
    }
    pause = () => {
        var route = BASE_URL + '/pausebot';
        var method = 'POST';
        console.log(this.props.setting)
        var botId = this.props.allSettings[this.props.selectedIndex]['id']
        var body = {
            "bot_id": botId,
            //"admin_pass": password
        }
        var request = $.ajax({
            url: route,
            method: method,
            data: body
        });

        request.done((data) => {
            console.log('paused')
        });
    }
    unpause = () => {
        var route = BASE_URL + '/unpausebot';
        var method = 'POST';
        console.log(this.props.setting)
        var botId = this.props.allSettings[this.props.selectedIndex]['id']
        var body = {
            "bot_id": botId,
            //"admin_pass": password
        }
        var request = $.ajax({
            url: route,
            method: method,
            data: body
        });

        request.done((data) => {
            console.log('paused')
        });
    }
    unpauseMultiple = () => {
        var route = BASE_URL + '/unpausebot';
        var method = 'POST';
        console.log(this.props.setting)
        Object.keys(this.props.selected).forEach((key) => {
            if (this.props.selected[key]) {
                var botId = this.props.allSettings[key]['id']
                var body = {
                    "bot_id": botId,
                    //"admin_pass": password
                }
                var request = $.ajax({
                    url: route,
                    method: method,
                    data: body
                });
                request.done((data) => {
                    console.log('paused')
                });
            }
        })

    }
    pauseMultiple = () => {
        var route = BASE_URL + '/pausebot';
        var method = 'POST';
        console.log(this.props.setting)
        Object.keys(this.props.selected).forEach((key) => {
            if (this.props.selected[key]) {
                var botId = this.props.allSettings[key]['id']
                var body = {
                    "bot_id": botId,
                    //"admin_pass": password
                }
                var request = $.ajax({
                    url: route,
                    method: method,
                    data: body
                });
                request.done((data) => {
                    console.log('paused')
                });
            }
        })

    }
    componentWillReceiveProps = (props) => {
        console.log(props.selectedIndex)
        console.log(props.type)
        if (props.selectedIndex != -1 && props.type == 1) {
            this.getLogs(props.selectedIndex)
        } else {
            this.setState({
                logs: "",
                setting: JSON.stringify(props.setting, null, 4),
            });
            return;
        }
        this.setState({
            setting: JSON.stringify(props.setting, null, 4),
        });
    }
    handleCountChange = (e) => {
        this.setState({
            count: e.target.value,
        })
    }
    handleSettingChange = (e) => {
        console.log(e.target.value);
        this.setState({
            setting: e.target.value,
        })
    }
    handleNameChange = (e) => {
        if (this.props.type == 0)
            this.setState({
                name: e.target.value,
            })
    }
    handleTypeChange = (e) => {
        this.setState({
            type: e.target.value,
            setting: JSON.stringify(bot_types[e.target.value], null, 4),
        })
    }
    render() {
        var options = Object.keys(bot_types).map(function(bot_type) {
            return <option value={bot_type}>{bot_type}</option>;
        });
        return (
            <div className="lol ui card">
                <div className="ui form">
                    <div className="field" rows="5" columns="40">
                        <textarea id="settingsText" className="setting-textarea" value={this.state.setting} onChange={this.handleSettingChange}></textarea>
                    </div>
                </div>
                {this.props.type == 0 && <div className="ui input">
                    <input value={this.state.name} placeholder={"Bot Name(ignored for multiple bot creation)"} onChange={this.handleNameChange}>
                    </input>
                </div>}
                <div className={"ui input"} >
                    <select className="select_style" value={this.state.type} placeholder="Bot Type" onChange={this.handleTypeChange}>
                        <option value="" selected disabled hidden>Choose here</option>
                        {options}
                    </select>
                </div>
                <div className="ui input" >
                    <input value={this.state.count} placeholder="Count" onChange={this.handleCountChange}>
                    </input>
                </div>
                <div className="ui">
                    <pre className="broken-paragraph">{
                        this.state.logs
                    }</pre>
                </div>
                {
                    this.props.type == 1 && <div className={"ui icon button add-bots " + this.props.hello} onClick={() => { this.props.modifyBot(this.state.setting) }}>
                        <i className="legal icon"></i>
                    </div>
                }
                {
                    this.props.type == 0 && <div className={"ui icon button add-bots " + this.props.hello} onClick={() => { this.props.add(this.state.name, this.state.type, this.state.setting, this.state.count) }}>
                        <i className="add icon"></i>
                    </div>
                }
                {
                    this.props.type == 1 && <div className={"ui icon button pause-bots " + this.props.hello} onClick={() => { this.pause() }}>
                        <i className="pause icon"></i>
                    </div>
                }
                {
                    this.props.type == 2 && <div className={"ui icon button pause-bots " + this.props.hello} onClick={() => { this.pauseMultiple() }}>
                        <i className="pause icon"></i>
                    </div>
                }
                {
                    this.props.type == 1 && <div className={"ui icon button play-bots " + this.props.hello} onClick={() => { this.unpause() }}>
                        <i className="play icon"></i>
                    </div>
                }
                {
                    this.props.type == 2 && <div className={"ui icon button play-bots " + this.props.hello} onClick={() => { this.unpauseMultiple() }}>
                        <i className="play icon"></i>
                    </div>
                }
                <div className={"ui icon button cancel-selection " + this.props.hello} onClick={this.props.cancel}>
                    <i className="cancel icon"></i>
                </div>
                <div className={"ui icon button refresh-selection " + this.props.hello} onClick={this.props.refresh}>
                    <i className="refresh icon"></i>
                </div>
            </div>
        );
    }
}