import AuthLayout from "../components/Layout/AuthLayout";
import FormLogin from "../components/Fragments/FormLogin";

const LoginPage = () =>{
    return (
        <AuthLayout title="Login">
            <FormLogin/>
        </AuthLayout>
    )
}

export default LoginPage;