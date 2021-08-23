import PageLayout from "../../Components/PageLayout";
import SignUpForm from "./SignUpForm";

export default function SignUpPage() {
  return (
    <PageLayout>
      <div className="flex flex-col justify-center h-full">
        <div className="w-1/3 border-2 border-blue-500 mx-auto p-8">
          <h2 className="font-bold text-lg text-center">회원가입</h2>
          <SignUpForm />
        </div>
      </div>
    </PageLayout>
  );
}
