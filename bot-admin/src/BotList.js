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
        this.setState({ selected: selected });
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
                    <input className="ui input" value={this.state.nameFilter} onChange={this.handleNameSearchChange} />
                </div>
                <div className="ui input field tag-search">
                    <input className="ui input" value={this.state.tagFilter} onChange={this.handleTagSearchChange} />
                </div>
                <div className={"ui icon button select-all black"} onClick={this.selectAll}>
                    <i className="check icon"></i>
                </div>
                <div className="botlist">
                    <table className="ui celled table">
                        <thead>
                            <tr>
                                <th>Id</th>
                                <th>Name</th>
                                <th>Type</th>
                                <th></th>
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
                                            <tr value={number} >
                                                <td>{this.props.settings[number]['id']}</td>
                                                <td>{this.props.settings[number]['name']}</td>
                                                <td onClick={(i) => { this.handleClick(number) }}>{this.props.settings[number]['type']}</td >
                                                <td className="collapsing">
                                                    <div className="ui fitted checkbox">
                                                        <input type="checkbox"
                                                            checked={this.state.selected[number]}
                                                            onClick={() => { this.handleToggle(number) }}
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