import './ManageGarantedCourses.scss'
import Table from 'react-bootstrap/Table';
import { useEffect, useState } from 'react';
import createRequest from '../../../Services/CreateRequest';
import LoadingIcon from '../../../Components/LoadingIcon/LoadingIcon';
import EditCourseModal from '../../../Components/EditCourseModal/EditCourseModal.jsx';
import { loggedUser } from '../../../Context/LoggedUser';
const ManageGarantedCourses = () => {
    const [courses, setCourses] = useState([])
    const [isLoading, setIsLoading] = useState(true)
    const [courseToEdit, setCourseToEdit] = useState({})
    const [modalOpen, setModalOpen] = useState(false)
    useEffect(()=> {
        setIsLoading(true);

        createRequest({
            path: '/get_garant_courses/' + loggedUser.id_person,
            method: 'GET'
        })
        .then(res => res.json())
        .then(res => {
            console.log(res)
            setIsLoading(false)
            setCourses(res)
        })
        .catch(err => {
            console.error(err)
            setIsLoading(false)
        })
    }, [])

    const editCourseModalOpen = (course) => {
        setCourseToEdit(course)
        setModalOpen(true)
    }

    const onEditCourse = (editedCourse) => {
        setCourses(prev => {
            return prev.map(el => el.id_course === editedCourse.id_course ? editedCourse : el)
        })
    }

    return (
        <>
            <>
        <h2>
            Manage courses where I'm garant
        </h2>
        <div align='center'>
            <div className='subjectsTableContainer'>
                <Table bordered>
                    <thead className='bg-info'>
                        <tr>
                            <th style={{width: '50px'}}>Abbrv</th>
                            <th>Title</th>
                            <th>Garant</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {isLoading ?
                            <tr>
                                <td colSpan={4} className={'text-center'}><LoadingIcon/></td>
                            </tr>
                            :
                            courses.map((el, idx) => {
                                return (
                                    <tr key={el.abbrv}>
                                        <td>{el.abbrv}</td>
                                        <td><a href={`/${el.aabrv}`}>{el.title}</a></td>
                                        <td>{el.garant.firstname} {el.garant.surname}</td>
                                        <td><a href={`#`} onClick={() => {editCourseModalOpen(el)}}>Edit</a></td>
                                    </tr>
                                )
                            })
                        }
                    </tbody>
                </Table>
            </div>
            <EditCourseModal isModalOpen={modalOpen} setModalOpen={setModalOpen} course={courseToEdit} sideEffectOnChange={onEditCourse}/>
        </div>
        </>
        </>
    )
}
export default ManageGarantedCourses