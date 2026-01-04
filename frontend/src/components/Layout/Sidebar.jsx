import { Menu } from "antd";
import { AppstoreOutlined } from "@ant-design/icons";

export default function Sidebar({ onSelect }) {
  return (
    <Menu
      style={{ width: 256 }}
      mode="inline"
      onClick={(item) => onSelect(item.key)}
      items={[
        {
          key: "sub1",
          label: "Сервис задач",
          icon: <AppstoreOutlined />,
          children: [
            {
              key: "g1",
              label: "Функционал",
              type: "group",
              children: [
                { key: "tasks", label: "Список всех задач" },
                { key: "create", label: "Создать задачу" },
              ],
            },
          ],
        },
      ]}
    />
  );
}
