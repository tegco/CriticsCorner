import React, { Component } from "react";
import { Container } from "reactstrap";
import axios from "axios";

import { API_URL_MOVIES } from "../constants"; 


function Home() {
    class Home extends Component {  //(14)
        state = {    //(15)
          questoes: []
        };
      
        componentDidMount() {    //(16)
          this.resetState();
        }
      
        getMovies = () => {
          axios.get(API_URL_MOVIES).then(res => this.setState({ movies:
      res.data }));    //(17)
        };

        resetState = () => {   
        //   this.getMovies();
        };
      
        render() {
          return (
            <Container style={{ marginTop: "20px" }}>
                <h1>hi</h1>
            </Container>
          );
        }
      }
}

export default Home;