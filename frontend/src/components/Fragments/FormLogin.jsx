import InputForm from "../Elements/Input";
import Button from "../Elements/Button"

const FormLogin = () => {
    return (
        <form action="">
        <InputForm
        label="Email"
        type="email"
        placeholder="example@email.com"
        name="email"
        />

        <InputForm
        label="Password"
        type="password"
        placeholder="****"
        name="password"
        />
        <Button variant="bg-blue-600 w-full">Login</Button>
        </form>
    )
};

export default FormLogin;