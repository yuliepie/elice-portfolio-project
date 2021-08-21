import Navigation from "./Navigation";
import styled from "styled-components";

export default function PageLayout({ children }) {
  return (
    <Layout>
      <header>
        <Navigation />
      </header>
      <main>{children}</main>
    </Layout>
  );
}

const Layout = styled.div`
  height: 100vh;
  background-color: pink;
`;
