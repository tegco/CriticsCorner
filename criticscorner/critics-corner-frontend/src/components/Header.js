import React, { useState } from "react";
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  NavbarText,
} from "reactstrap";

function Header(args) {
  const [isOpen, setIsOpen] = useState(true);

  const toggle = () => setIsOpen(!isOpen);

  return (
    <div>
      <Navbar {...args} className="my-2" color="dark" dark>
        <NavbarBrand href="/">
          <img
            src="https://www.northstar-alliance.org/wp-content/uploads/2015/07/movie-icon.png"
            style={{
              height: 50,
              width: 50,
              padding: 5,
            }}
          />
          Critic's Corner
        </NavbarBrand>
        <Nav className="me-auto" navbar>
          <NavItem>
            <NavLink href="/Top250">Top 250</NavLink>
          </NavItem>
          {/* <NavItem>
              <NavLink href="https://github.com/reactstrap/reactstrap">
                GitHub
              </NavLink>
            </NavItem> */}
        </Nav>
        <NavbarToggler onClick={toggle} />
        <Collapse isOpen={isOpen} navbar>
          <Nav className="me-auto" navbar></Nav> 
        </Collapse>
      </Navbar>
    </div>
  );
}
export default Header;
