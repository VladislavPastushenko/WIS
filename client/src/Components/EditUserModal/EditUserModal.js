import './EditUserModal.scss'
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import createRequest from '../../Services/CreateRequest';
import { toast , ToastContainer} from 'react-toastify';
import { useContext } from 'react';
import { LoggedUserContext } from '../../Context/LoggedUser';
const EditUserModal = ({isModalOpen, setModalOpen, user, sideEffectOnChange}) => {
    const {loggedUser, setLoggedUser} = useContext(LoggedUserContext)
    const onSubmit = (e) => {
        e.preventDefault()

        // if (e.target.password.value === e.target.passwordRepeat.value) {
        const data = {
            ...user,
        }
        if (e.target.firstname) data.firstname = e.target.firstname.value;
        if (e.target.surname) data.surname = e.target.surname.value;
        if (e.target.email) data.email = e.target.email.value;
        if (e.target.address) data.address = e.target.address.value;
        if (e.target.telephone) data.telephone = e.target.telephone.value;
        if (e.target.role) data.role = e.target.role.value;

        createRequest({
            path: '/profile_edit/' + user.id_person,
            method: 'POST',
            body: JSON.stringify(data)
        })
        .then(res => {
            if (sideEffectOnChange) sideEffectOnChange(data)
            toast.success('User was successfully edited')
            setModalOpen(false)
        })
        .catch(err => {
            toast.error('Something went wrong')
            console.log(err)
        })

    }

    return (
        <>
        <ToastContainer/>
        <Modal show={isModalOpen} onHide={() => {setModalOpen(false)}}>
            <Modal.Header closeButton>
                <Modal.Title>Edit user</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form className={'signUpForm'} onSubmit={e => {onSubmit(e)}} id={'Edit' + user.username}>
                    <Form.Group className="mb-3">
                        <Form.Label>First Name</Form.Label>
                        <Form.Control type="text" name='firstname' placeholder="Name" defaultValue={user.firstname}/>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Last Name</Form.Label>
                        <Form.Control type="text" name='surname' placeholder="Last name" defaultValue={user.surname}/>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="email" name='email' placeholder="example@mail.com" defaultValue={user.email}/>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Address</Form.Label>
                        <Form.Control type="text" name='address' placeholder="Brno, Kolejni 2" defaultValue={user.address}/>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Phone number</Form.Label>
                        <Form.Control type="text" name='telephone' placeholder="+420(777)777-777" defaultValue={user.telephone}/>
                    </Form.Group>

                    {loggedUser.role === 'a' &&
                    <Form.Group className="mb-3">
                        <Form.Label>Role</Form.Label>
                        <Form.Select name='role' defaultValue={user.role}>
                            <option value={'a'}>Administrator</option>
                            <option value={'g'}>Garant</option>;
                            <option value={'l'}>Lektor</option>;
                            <option value={'s'}>Student</option>;
                        </Form.Select>
                    </Form.Group>
                    }
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={() => {setModalOpen(false)}}>
                    Close
                </Button>
                <Button type='submit' variant="primary" form={'Edit' + user.username}>
                    Save Changes
                </Button>
            </Modal.Footer>
        </Modal>
        </>
    )
}
export default EditUserModal;