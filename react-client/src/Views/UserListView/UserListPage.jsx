import PageLayout from "../../Components/PageLayout";
import { useAuth } from "../../Contexts/authContext";

export default function UserListPage() {
  const { currentUser } = useAuth();
  console.log("current user: ", currentUser);

  return (
    <PageLayout>
      <div>User List!!!</div>
    </PageLayout>
  );
}
