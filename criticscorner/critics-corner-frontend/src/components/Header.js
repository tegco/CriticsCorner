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
import logo from "../images/Logo-idea-2-removebg-preview.png";

function Header(args) {
  const [isOpen, setIsOpen] = useState(true);

  const toggle = () => setIsOpen(!isOpen);

  return (
    <div>
      <Navbar {...args} className="my-2" color="black" dark>
        <NavbarBrand href="/">
          <img
            src={logo}
            style={{
              height: 80,
              padding: 5,
            }}
          />
          Top Rated
        </NavbarBrand>
        <Nav className="me-auto" navbar>
          <NavItem>
            <NavLink href="http://localhost:8000">
              Home
            </NavLink>
          </NavItem>
        </Nav>
      </Navbar>
    </div>
  );
}
export default Header;
