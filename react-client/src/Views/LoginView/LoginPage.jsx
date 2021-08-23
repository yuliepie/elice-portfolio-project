import PageLayout from "../../Components/PageLayout";
import LoginForm from "./LoginForm";

export default function LoginPage() {
  return (
    <PageLayout>
      <div className="flex flex-col justify-center h-full">
        <div className="w-1/3 border-2 border-blue-500 mx-auto p-8">
          <h2 className="font-bold text-lg text-center">로그인</h2>
          <LoginForm />
        </div>
      </div>
    </PageLayout>
  );
}
