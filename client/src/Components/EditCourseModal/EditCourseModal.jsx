import './EditCourseModal.scss'
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import createRequest from '../../Services/CreateRequest';
import { toast , ToastContainer} from 'react-toastify';
import { useContext, useEffect, useState } from 'react';
import { LoggedUserContext } from '../../Context/LoggedUser';
import LoadingIcon from '../LoadingIcon/LoadingIcon';
const EditCourseModal = ({isModalOpen, setModalOpen, course, sideEffectOnChange}) => {
    const {loggedUser, setLoggedUser} = useContext(LoggedUserContext)
    const [isLoadingGarants, setIsLoadingGarants] = useState(true)
    const [garants, setGarants] = useState([])

    const [isLoadingTeachers, setIsLoadingTeachers] = useState(true)
    const [teachers, setTeachers] = useState([])
    const [selectedTeachers, setSelectedTeachers] = useState([])

    useEffect(() => {
        if (course.lectors && course.lectors.length !== 0)
            setSelectedTeachers(course.lectors.map(el => el.id_teacher_id))
        else setSelectedTeachers([])
    }, [course.lectors])

    const onSubmit = (e) => {
        e.preventDefault()

        const data = {
            ...course,
        }
        if (e.target.abbrv) data.abbrv = e.target.abbrv.value;
        if (e.target.title) data.title = e.target.title.value;
        if (e.target.description) data.description = e.target.description.value;
        if (e.target.credits) data.credits = parseInt(e.target.credits.value);
        if (e.target.max_persons) data.max_persons = parseInt(e.target.max_persons.value);
        if (e.target.type) data.type = e.target.type.value;
        if (e.target.approved) data.approved = e.target.approved.value === 'true';
        if (e.target.garant_id) data.garant_id = parseInt(e.target.garant_id.value);
        data.lectors_id = selectedTeachers.map(el => parseInt(el))


        createRequest({
            path: '/course-edit/' + course.id_course,
            method: 'POST',
            body: JSON.stringify(data)
        })
        .then(res => {
            if (sideEffectOnChange) sideEffectOnChange({...data, garant: garants.find(el => el.id_person === data.garant_id)})
            toast.success('Course was successfully edited')
            setModalOpen(false)
        })
        .catch(err => {
            toast.error('Something went wrong')
            console.log(err)
        })
    }

    useEffect(() => {
        setIsLoadingGarants(true)
        createRequest({
            path: '/get-all-users?role=g',
            method: 'GET',
        })
        .then(res => res.json())
        .then(res => {
            setIsLoadingGarants(false)
            setGarants(res)
        })
        .catch(err => {
            console.error(err)
            setIsLoadingGarants(false)
        })

        setIsLoadingTeachers(true)
        createRequest({
            path: '/get-all-users?role=l',
            method: 'GET',
        })
        .then(res => res.json())
        .then(res => {
            setIsLoadingTeachers(false)
            setTeachers(res)
        })
        .catch(err => {
            console.error(err)
            setIsLoadingTeachers(false)
        })

    }, [])


    const selectTeacher = (idx, newValue) => {
        setSelectedTeachers(prev => prev.map((el, prevIdx) => prevIdx === idx ? newValue : el))
    }

    const removeTeacher = (idx) => {
        setSelectedTeachers(prev => prev.filter((el, prevIdx) => prevIdx !== idx))
    }

    const addTeacher = (idx) => {
        setSelectedTeachers(prev => [...prev, teachers[0].id_person])
    }

    return (
        <>
        <ToastContainer/>
        <Modal show={isModalOpen} onHide={() => {setModalOpen(false)}}>
            <Modal.Header closeButton>
                <Modal.Title>Edit course</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form className={'editCourseForm'} onSubmit={e => {onSubmit(e)}} id={'Edit course' + course.id_course}>
                    <Form.Group className="mb-3">
                        <Form.Label>Abbreviation</Form.Label>
                        <Form.Control type="text" name='abbrv' placeholder="IXX" defaultValue={course.abbrv}/>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Title</Form.Label>
                        <Form.Control type="text" name='title' placeholder="Name of course" defaultValue={course.title}/>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Description</Form.Label>
                        <Form.Control as='textarea' rows={3} name='description' placeholder="Name of course" defaultValue={course.description}/>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Credits</Form.Label>
                        <Form.Control type={'number'} min={1} max={15} name='credits' placeholder="2" defaultValue={course.credits}/>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Max students</Form.Label>
                        <Form.Control type={'number'} min={1} max={1000} name='max_persons' placeholder="100" defaultValue={course.max_persons}/>
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Winter or summer</Form.Label>
                        <Form.Select name='type' defaultValue={course.type}>
                            <option value={'w'}>Winter</option>
                            <option value={'s'}>Summer</option>;
                        </Form.Select>
                    </Form.Group>

                    {loggedUser.role === 'a' &&
                        <Form.Group className="mb-3">
                            <Form.Label>Garant</Form.Label>
                            {isLoadingGarants ?
                            <p><LoadingIcon/></p>
                            :
                            <Form.Select name='garant_id' defaultValue={course.approved}>
                                {garants.map(el =>
                                    <option  value={el.id_person} key={el.id_person + 'garant'}>
                                        {el.firstname} {el.surname}
                                    </option>
                                )}
                            </Form.Select>}
                        </Form.Group>
                    }

                    <Form.Group className="mb-3">
                        <Form.Label>Teachers</Form.Label>
                        {isLoadingTeachers ?
                            <p><LoadingIcon/></p>
                            :
                            <>
                            {selectedTeachers && selectedTeachers.map((selectedTeacher, idx) => {
                                return (
                                    <>
                                    <Form.Select defaultValue={selectedTeacher} onChange={(e) => {selectTeacher(idx, e.currentTarget.value)}}>
                                        {teachers.map(el =>
                                            <option value={el.id_person} key={el.id_person + 'teacher'}>
                                                {el.firstname} {el.surname}
                                            </option>
                                        )}
                                    </Form.Select>
                                    <div style={{marginBottom: '1em'}}>
                                        <a href="#" onClick={() => {removeTeacher(idx)}}>Remove</a>
                                    </div>
                                    </>
                                    )
                                })
                            }
                            <div>
                                <a href="#" onClick={() => {addTeacher()}}> Add </a>
                            </div>
                            </>
                        }
                    </Form.Group>

                    {loggedUser.role === 'a' &&
                    <Form.Group className="mb-3">
                        <Form.Label>Is approved</Form.Label>
                        <Form.Select name='approved' defaultValue={course.approved}>
                            <option value={true}>Approved</option>
                            <option value={false}>Not approved</option>;
                        </Form.Select>
                    </Form.Group>
                    }
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={() => {setModalOpen(false)}}>
                    Close
                </Button>
                <Button type='submit' variant="primary" form={'Edit course' + course.id_course}>
                    Save Changes
                </Button>
            </Modal.Footer>
        </Modal>
        </>
    )
}
export default EditCourseModal;