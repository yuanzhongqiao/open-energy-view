import React, { useState, useEffect } from "react";
import cookie from "react-cookies";
import { Form, Button, DropdownButton, Dropdown } from "react-bootstrap";

const SourceRegistration = (props) => {
  const [form, setForm] = useState("");
  const [name , setName] = useState("");
  const [thirdPartyId, setThirdPartyId] = useState("");
  const [clientId, setClientId] = useState("");
  const [clientSecret, setClientSecret] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
  }

  const initialForm = (
    <div className="register-box">
      <Form.Text className="form-title">Add New Data Source</Form.Text>
      <hr />
      <DropdownButton
        onSelect={(e) => showPge(e)}
        id="dropdown-basic-button"
        title="Select Source"
      >
        <Dropdown.Item eventKey="pge">PG&E</Dropdown.Item>
      </DropdownButton>
    </div>
  );

  const pgeForm = (
    <div className="register-box">
      <Form onSubmit={handleSubmit}>
      <Form.Text className="form-title">PG&E Share My Data</Form.Text>
      <Form.Text className="form-title">Self Access</Form.Text>
        <Form.Group controlId="formPge">
        <Form.Label>Name</Form.Label>
          <Form.Control
            className="login-form"
            type="text"
            placeholder="Name, like PG&E or Home PG&E"
            onChange={(e) => setName(e.target.value)}
          />
          <Form.Label>Third-Party ID</Form.Label>
          <Form.Control
            className="login-form"
            type="text"
            placeholder="Third-Party ID"
            onChange={(e) => setThirdPartyId(e.target.value)}
          />
          <Form.Label>Client ID</Form.Label>
          <Form.Control
            className="login-form"
            type="text"
            placeholder="Client ID"
            onChange={(e) => setClientId(e.target.value)}
          />
          <Form.Label>Client Secret</Form.Label>
          <Form.Control
            className="login-form"
            type="text"
            placeholder="Client Secret"
            onChange={(e) => setClientSecret(e.target.value)}
          />
        </Form.Group>
        <Button variant="primary" type="submit">
          Add Source
        </Button>
        <hr />
      </Form>
    </div>
  );

  useEffect(() => {
    setForm(initialForm);
  }, []);

  const showPge = (e) => {
    switch (e) {
      case "pge":
        setForm(pgeForm);
        break;
    }
  };

  return form;
};

export default SourceRegistration;
