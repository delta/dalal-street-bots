import React, { Component } from 'react';
import './index.css'
import $ from 'jquery'

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
        var route = "http://192.168.100.5:9999/proxy/http://192.168.100.5:5000" + '/getlogs';
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
            Object.keys(x).forEach((val) => {
                y += (x[val]) + " \n "
            })
            console.log(y)
            this.setState({
                logs: y
            });
        });
    }
    pause = () => {
        var route = "http://192.168.100.5:9999/proxy/http://192.168.100.5:5000" + '/pausebot';
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
        var route = "http://192.168.100.5:9999/proxy/http://192.168.100.5:5000" + '/unpausebot';
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
        var route = "http://192.168.100.5:9999/proxy/http://192.168.100.5:5000" + '/unpausebot';
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
        var route = "http://192.168.100.5:9999/proxy/http://192.168.100.5:5000" + '/pausebot';
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
                setting: JSON.stringify(props.setting),
            });
            return;
        }
        this.setState({
            setting: JSON.stringify(props.setting),
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
        if (this.props.type == 0)
            this.setState({
                type: e.target.value,
            })
    }
    render() {
        return (
            <div className="lol ui card">
                <div className="ui input textarea" rows="5" columns="40">
                    <textarea value={this.state.setting} onChange={this.handleSettingChange}></textarea>
                </div>
                {this.state == 0 && <div className={"ui input"}>
                    <input value={this.state.name} onChange={this.handleNameChange}>
                    </input>
                </div>}
                <div className={"ui input"}>
                    <input value={this.state.type} onChange={this.handleTypeChange}>
                    </input>
                </div>
                <div className="ui input">
                    <input value={this.state.count} onChange={this.handleCountChange}>
                    </input>
                </div>
                <div class="ui bottom attached segment pushable grid">
                    <div class="pusher grid">
                        <div class="ui main text container small">
                            <pre className="broken-paragraph">{
                                this.state.logs
                            }</pre>
                        </div>
                    </div>
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