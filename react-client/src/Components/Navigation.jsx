import { NavLink } from "react-router-dom";
import styled from "styled-components";

export default function Navigation() {
  return (
    <Nav>
      <NavLink to="/">Home</NavLink>
      <NavLink to="/about">About</NavLink>
      <NavLink to="/contact">Contact</NavLink>
    </Nav>
  );
}

const Nav = styled.div`
  padding: 24px;
  & > a:not(:first-of-type) {
    margin-left: 200px;
  }
`;
