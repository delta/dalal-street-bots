import React from 'react';
import App from './App'

export class BotList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selected: this.props.selected,
            nameFilter: "",
            tagFilter: "",
        }
    }
    componentWillReceiveProps = (props)=>{
        console.log(props)
        this.setState({
            selected:props.selected
        })
    }
    handleClick = (i) => {
        this.props.handleSingleSelect(i)
    }
    handleToggle = (number) => {
        let selected = this.state.selected.slice();
        selected[number] = !selected[number];
        this.props.selectAll(selected)
    }
    handleNameSearchChange = (e) => {
        this.setState({
            nameFilter: e.target.value
        })
    }
    handleTagSearchChange = (e) => {
        this.setState({
            tagFilter: e.target.value
        })
    }
    selectAll = () => {
        let selected = this.state.selected.slice();
        console.log(selected)
        this.props.numbers.map((number) => {
            let x = this.props.settings[number]['name'];
            let y = this.props.settings[number]['settings']['tag']
            if (!y && this.state.tagFilter != "")
                return;
            if (y && y.indexOf(this.state.tagFilter) === -1)
                return;
            if (x.indexOf(this.state.nameFilter) !== -1) {
                selected[number] = true;
                return;
            }
            selected[number] = false;
        })
        this.props.selectAll(selected)
    }
    render() {
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
                                <th onClick={this.selectAll}><i className="check icon"></i></th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                this.props.numbers.map((number) => {
                                    console.log(this.state.selected)
                                    console.log(number)
                                    let x = this.props.settings[number]['name']
                                    let y = this.props.settings[number]['settings']['tag']
                                    if (!y && this.state.tagFilter != "")
                                        return;
                                    if (y && y.indexOf(this.state.tagFilter) === -1)
                                        return;
                                    if (x.indexOf(this.state.nameFilter) !== -1) {
                                        return (
                                            <tr value={number}  onClick={(i) => { this.handleClick(number) }}>
                                                <td>{this.props.settings[number]['id']}</td>
                                                <td>{this.props.settings[number]['name']}</td>
                                                <td>{this.props.settings[number]['type']}</td >
                                                <td>{this.props.settings[number]['settings']['tag']}</td >
                                                <td className="collapsing">
                                                    <div className="ui fitted checkbox">
                                                        <input type="checkbox"
                                                            checked={this.state.selected[number]}
                                                            onClick={(e) => { this.handleToggle(number);e.stopPropagation()}}
                                                        />
                                                        <label></label>
                                                    </div>
                                                </td>
                                            </tr>
                                        )
                                    }
                                }
                                )
                            }
                        </tbody>
                    </table>
                </div>
            </div>
        );
    }
}