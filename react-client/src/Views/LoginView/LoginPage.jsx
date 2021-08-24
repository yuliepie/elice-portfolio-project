import PageLayout from "../../Components/PageLayout";
import LoginForm from "./LoginForm";

export default function LoginPage() {
  return (
    <PageLayout>
      <div className="bg-indigo-500 bg-opacity-80 flex flex-col py-16 justify-start items-center h-full">
        <h2 className="header-text font-extrabold">로그인하세요.</h2>
        <div className="w-auto mt-8 p-8 bg-white rounded-xl shadow-md">
          <LoginForm />
        </div>
      </div>
    </PageLayout>
  );
}
