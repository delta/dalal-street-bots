import React from 'react';

export class BotList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            nameFilter: "",
            tagFilter: "",
        }
    }
    // search based on name
    handleNameSearchChange = (e) => {
        this.setState({
            nameFilter: e.target.value
        })
    }
    // search based on tag
    handleTagSearchChange = (e) => {
        this.setState({
            tagFilter: e.target.value
        })
    }
    // this is called when the header is clicked to select all
    selectAll = () => {
        let newBotList = this.props.botList.filter((botObj) => {
            return botObj['name'].includes(this.state.nameFilter)
        }).map((botObj) => {
            return botObj['id'];
        });
        this.props.handleSelection(newBotList);
    }

    getBotList(botList) {
        let newBotList = botList.filter((botObj) => {
            return botObj['name'].includes(this.state.nameFilter);
        }).map((botObj) => {
            let botId = botObj['id'];
            let botArr = [botId];
                return (
                    <tr value={botId}>
                        <td>{botObj['id']}</td>
                        <td>{botObj['name']}</td>
                        <td>{botObj['type']}</td >
                        <td>{botObj['settings']['tag'] ? botObj['settings']['tag'] : ''}</td >
                        <td>{botObj['is_paused'] === 0 ? "Active": "Paused"}</td >
                        <td className="collapsing">
                            <div className="ui fitted checkbox">
                                <input type="checkbox"
                                    checked={this.props.selected[botId]}
                                    onClick={(botId) => { this.props.handleSelection(botArr); return }}
                                />
                                <label></label>
                            </div>
                        </td>
                    </tr>
                );
        });
        return newBotList;
    }

    render() {
        let botList = this.getBotList(this.props.botList);
        return (
            <div>
                <div className="ui input field name-search">
                    <input className="ui input" placeholder="Name"value={this.state.nameFilter} onChange={this.handleNameSearchChange} />
                </div>
                <div className="ui input field tag-search">
                    <input className="ui input" placeholder="Tag" value={this.state.tagFilter} onChange={this.handleTagSearchChange} />
                </div>
                <div className="botlist">
                    <table className="ui celled table">
                        <thead>
                            <tr>
                                <th>Id</th>
                                <th>Name</th>
                                <th>Type</th>
                                <th>Tag</th>
                                <th>Status</th>
                                <th onClick={this.selectAll}><i className="check icon"></i></th>
                            </tr>
                        </thead>
                        <tbody>
                            {botList}
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }
}