import React from 'react';
import PNotify from 'pnotify/dist/es/PNotify';
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
    },
    'MarketmakerBot': {
        "sleep_duration": 15, // in seconds. THIS SETTING IS REQUIRED
        "no_of_companies": 15, // number of companies to buy from. Technically should be ALL
        "bot_tag": "unset", // special tags for searching purpose
        "e_start": 2, // value of e will go from [e_start, e_end]
        "e_end": 4, // value of e will go from [e_start, e_end]
        "percent_diff": 2 // if bid spread percent is less than this, do nothing
    },
    'ModernportfolioBot': {
        "sleep_duration": 15, // in seconds. THIS SETTING IS REQUIRED
        "no_of_companies": 15, // number of companies to buy from. Technically should be ALL
        "bot_tag": "unset", // special tags for searching purpose
        "n": 6, // number of companies for the buy-and-hold strategy
        'lookup_window': 5,  // number of entries to look for in indicator
        'trade_wait_duration': 5,  // amount to wait before you can sell whatever you bought
    },
};

export class Panel extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            setting: JSON.stringify(this.props.botList, null, 4),
            name: "",
            type: "",
            logs: "",
            count: 1,
        }
    }

    getBotObj = (botId) => {
        let botList = this.props.botList;
        let botObj = {};
        for (let i = 0; i< botList.length; i++) {
            if (botList[i]['id'] == botId) {
                botObj = botList[i];
            }
        }
        return botObj;
    }

    getLogs = function (botId) {
        let route = BASE_URL + '/getlogs';
        let method = 'POST';
        let body = {
            "bot_id": botId,
        };
        let request = $.ajax({
            url: route,
            method: method,
            data: body
        });

        request.done((data) => {
            let x = JSON.parse(data);
            let y = "";
            Object.keys(x).map((val) => {
                y += x[val][2] + " : " + x[val][1] + "\n"
            })
            this.setState({
                logs: y
            });
        });
    }

    unpause = () => {
        let route = BASE_URL + '/unpausebot';
        let method = 'POST';
        Object.keys(this.props.selected).forEach((key) => {
            if (this.props.selected[key]) {
                let botId = key;
                let body = {
                    "bot_id": botId,
                }
                let request = $.ajax({
                    url: route,
                    method: method,
                    data: body
                });
                request.done((data) => {
                });
            }
        });
        let isPaused = false;
        this.props.togglePaused(isPaused);
    }

    pause = () => {
        let route = BASE_URL + '/pausebot';
        let method = 'POST';
        let count = 0;
        Object.keys(this.props.selected).forEach((key) => {
            if (this.props.selected[key]) {
                let botId = key;
                let body = {
                    "bot_id": botId,
                }
                let request = $.ajax({
                    url: route,
                    method: method,
                    data: body
                });
                request.done((data) => {
                    count = count + 1;
                });
            }
        });
        let isPaused = true;
        this.props.togglePaused(isPaused);
    }

    componentWillReceiveProps = (props) => {
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
        this.setState({
            setting: e.target.value,
        })
    }

    handleNameChange = (e) => {
        this.setState({
            name: e.target.value,
        });
    }

    handleTypeChange = (e) => {
        this.setState({
            type: e.target.value,
            setting: JSON.stringify(bot_types[e.target.value], null, 4),
        })
    }

    render() {
        let options = Object.keys(bot_types).map(function(bot_type) {
            return <option key={"options-" + bot_type} value={bot_type}>{bot_type}</option>;
        })
        let isEmpty = Object.values(this.props.selected).every((bool) => { return bool == false;});
        return (
            <div className="lol ui card">
                <div className="ui form">
                    <div className="field" rows="5" columns="40">
                        <textarea id="settingsText" className="setting-textarea" value={this.state.setting} onChange={this.handleSettingChange}></textarea>
                    </div>
                </div>

                <div className="ui input">
                    <input value={this.state.name} placeholder="Bot Name(ignored for multiple bot creation)" onChange={this.handleNameChange}>
                    </input>
                </div>

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
                    <pre className="broken-paragraph">{this.state.logs}</pre>
                </div>
                {
                    !isEmpty && <div data-tooltip="Modify selected bots according to your new configurations" className={"ui icon button add-bots " + this.props.color} onClick={() => { this.props.modifyBot(this.state.setting) }}>
                        <i className="legal icon"></i>
                    </div>
                }
                {
                    isEmpty && <div data-tooltip="Add new bots" className={"ui icon button add-bots " + this.props.color} onClick={() => { this.props.add(this.state.name, this.state.type, this.state.setting, this.state.count) }}>
                        <i className="add icon"></i>
                    </div>
                }

                {
                    !isEmpty && <div data-tooltip="Pause selected bots" className={"ui icon button pause-bots " + this.props.color} onClick={() => { this.pause() }}>
                        <i className="pause icon"></i>
                    </div>
                }

                {
                    !isEmpty && <div data-tooltip="Unpause selected bots" className={"ui icon button play-bots " + this.props.color} onClick={() => { this.unpause() }}>
                        <i className="play icon"></i>
                    </div>
                }

                <div data-tooltip="Reset back to normal" className={"ui icon button cancel-selection " + this.props.color} onClick={this.props.cancel}>
                    <i className="cancel icon"></i>
                </div>

                <div data-tooltip="Refresh page" className={"ui icon button refresh-selection " + this.props.color} onClick={this.props.refresh}>
                    <i className="refresh icon"></i>
                </div>
            </div>
        );
    }
}