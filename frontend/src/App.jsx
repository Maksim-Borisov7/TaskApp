import { useState } from "react";
import Sidebar from "./components/Layout/Sidebar";
import TasksList from "./pages/TasksList";
import CreateTask from "./pages/CreateTask";
import LoginRegister from "./pages/LoginRegister";

export default function App() {
  const [stage, setStage] = useState("auth");
  const [page, setPage] = useState("tasks");

  if (stage === "auth") {
    return <LoginRegister onLoginSuccess={() => setStage("app")} />;
  }

  return (
    <div style={{ display: "flex" }}>
      <Sidebar onSelect={setPage} />

      <div style={{ padding: 20, flex: 1 }}>
        {page === "tasks" && <TasksList />}
        {page === "create" && <CreateTask onCreated={() => setPage("tasks")} />}
      </div>
    </div>
  );
}
