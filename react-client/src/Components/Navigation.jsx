import { NavLink } from "react-router-dom";
import styled from "styled-components";
import { Menu } from "antd";

export default function Navigation() {
  return (
    <>
      <div className="logo"></div>
      <Menu theme="dark" mode="horizontal">
        <Menu.Item key="Network">
          <NavLink to="/">Networks</NavLink>
        </Menu.Item>
        <Menu.Item key="MyPage">
          <NavLink to="/myPage">My Page</NavLink>
        </Menu.Item>
        <Menu.Item key="Login">
          <NavLink to="/login">Log In</NavLink>
        </Menu.Item>
      </Menu>
    </>
  );
}

const Nav = styled.div`
  padding: 24px;
  & > a:not(:first-of-type) {
    margin-left: 200px;
  }
`;
