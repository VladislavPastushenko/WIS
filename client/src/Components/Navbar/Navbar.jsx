import { Link, useLocation } from "react-router-dom"
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import './Navbar.scss'
import { useContext, useEffect, useState } from "react";
import { LoggedUserContext } from "../../Context/LoggedUser";

const Header = () => {
    const location = useLocation().pathname
    const {loggedUser, setLoggedUser} = useContext(LoggedUserContext)
    const [isLoggedIn, setIsLoggedIn] = useState(!!loggedUser.token)

    useEffect(() => {
        setIsLoggedIn(!!loggedUser.token)
    }, [loggedUser])
    return (
        <Navbar bg="light" expand="lg">
            <Container className="navbar-container">
                <Navbar.Brand href="/">
                    <h4 className="fw-normal">
                        Home page
                    </h4>
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="ms-auto">
                    <Nav.Link href="/"> Home </Nav.Link>
                    {!isLoggedIn &&
                    <>
                    <Nav.Link href="/login">Login</Nav.Link>
                    <Nav.Link href="/sign-up">Sign-up</Nav.Link>
                    </>
                    }
                    {isLoggedIn &&
                    <Nav.Link href="/my-profile"> My profile</Nav.Link>
                    }
                    {loggedUser.role === 'a' &&
                    <Nav.Link href="/admin"> Admin </Nav.Link>
                    }
                </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    )
}

export default Header