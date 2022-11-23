import './Home.scss'
import Table from 'react-bootstrap/Table';
import { useEffect, useState } from 'react';
import createRequest from '../../Services/CreateRequest';
import LoadingIcon from '../../Components/LoadingIcon/LoadingIcon';

function Home() {
    const [courses, setCourses] = useState([])
    const [isLoading, setIsLoading] = useState(true)

    useEffect(()=> {
        setIsLoading(true);

        createRequest({
            path: '/get-courses',
            method: 'GET'
        })
        .then(res => res.json())
        .then(res => {
            setIsLoading(false)
            setCourses(res)
        })
        .catch(err => {
            console.err(err)
            setIsLoading(false)
        })
    }, [])
    return (
        <>
        <h2>
            Home
        </h2>
        <div align='center'>
            <div className='subjectsTableContainer'>
                <Table bordered>
                    <thead className='bg-info'>
                        <tr>
                            <th style={{width: '50px'}}>Abbrv</th>
                            <th>Title</th>
                            <th style={{width: '150px'}}>Duty</th>
                            <th style={{width: '150px'}}>Fakulta</th>
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
                                        <td>{el.credits}</td>
                                        <td>{el.fakulta}</td>
                                    </tr>
                                )
                            })
                        }
                    </tbody>
                </Table>
            </div>
        </div>
        </>
    );
}

export default Home;