import Navigation from "./Navigation";
import styled from "styled-components";
import { Layout } from "antd";

export default function PageLayout({ children }) {
  const { Header, Content, Footer } = Layout;
  return (
    <Layout className="layout">
      <Header>
        <Navigation />
      </Header>
      <Layout className="layout">
        <Content className="content">
          <main className="site-layout-content">{children}</main>
        </Content>
      </Layout>
      <Footer className="footer">Footer</Footer>
    </Layout>
  );
}
