import React, { Component } from "react";
import { Container } from "reactstrap";
import axios from "axios";

import { API_URL_MOVIES } from "../constants";
import DisplayMovies from "./DisplayMovies";

class Home extends Component {
  state = {
    movies: [],
  };

  componentDidMount() {
    this.resetState();
  }

  getMovies = () => {
    axios.get(API_URL_MOVIES).then((res) => {
      console.log("TESTE 2");
      console.log(res.data);
      this.setState({ movies: res.data });
    });
  };

  resetState = () => {
    console.log("TESTE 1");
    this.getMovies();
  };

  render() {
    return (
      <Container style={{ marginTop: "100px" }}>
        {/* <DisplayMovies movies={this.state.movies} /> */}
      </Container>
    );
  }
}

export default Home;
