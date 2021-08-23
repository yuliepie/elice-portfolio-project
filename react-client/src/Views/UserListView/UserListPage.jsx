import PageLayout from "../../Components/PageLayout";
import { useAuth } from "../../Contexts/authContext";
import axios from "axios";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";

export default function UserListPage() {
  return (
    <PageLayout>
      <div>User List Page!!!</div>
    </PageLayout>
  );
}
