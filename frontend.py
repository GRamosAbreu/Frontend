import flet as ft
import httpx

API_URL = "https://pagina-web-52ih.onrender.com"  # Ajusta según donde corra tu backend

async def main(page: ft.Page):
    page.title = "Gestión de Usuarios"
    page.scroll = "adaptive"
    
    username = ft.TextField(label="Usuario", width=300)
    contrasena = ft.TextField(label="Contraseña (número)", width=300, password=True)
    id_field = ft.TextField(label="ID Usuario", width=300)
    output = ft.Column()

    async def crear_usuario(e):
        async with httpx.AsyncClient() as client:
            try:
                r = await client.post(f"{API_URL}/crear-usuario", json={
                    "username": username.value,
                    "contrasena": int(contrasena.value)
                })
                if r.status_code == 200:
                    output.controls.append(ft.Text("✅ Usuario creado correctamente"))
                else:
                    output.controls.append(ft.Text(f"⚠️ Error: {r.text}"))
            except Exception as ex:
                output.controls.append(ft.Text(f"❌ {ex}"))
            page.update()

    async def listar_usuarios(e):
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{API_URL}/usuarios")
            if r.status_code == 200:
                usuarios = r.json()
                output.controls.clear()
                for u in usuarios:
                    output.controls.append(ft.Text(f"👤 {u}"))
            else:
                output.controls.append(ft.Text(f"⚠️ Error: {r.text}"))
            page.update()

    async def ver_usuario(e):
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{API_URL}/usuario/{id_field.value}")
            output.controls.clear()
            output.controls.append(ft.Text(r.text))
            page.update()

    async def borrar_usuario(e):
        async with httpx.AsyncClient() as client:
            r = await client.delete(f"{API_URL}/borrar/{id_field.value}")
            output.controls.append(ft.Text(r.text))
            page.update()

    async def reemplazar_usuario(e):
        async with httpx.AsyncClient() as client:
            r = await client.put(f"{API_URL}/remplazar", params={"id": id_field.value}, json={
                "username": username.value,
                "contrasena": int(contrasena.value)
            })
            output.controls.append(ft.Text(r.text))
            page.update()

    page.add(
        ft.Text("Gestión de Usuarios", size=30, weight="bold"),
        username,
        contrasena,
        id_field,
        ft.Row([
            ft.ElevatedButton("Crear Usuario", on_click=crear_usuario),
            ft.ElevatedButton("Listar Usuarios", on_click=listar_usuarios),
        ]),
        ft.Row([
            ft.ElevatedButton("Ver Usuario por ID", on_click=ver_usuario),
            ft.ElevatedButton("Borrar Usuario", on_click=borrar_usuario),
            ft.ElevatedButton("Reemplazar Usuario", on_click=reemplazar_usuario),
        ]),
        ft.Divider(),
        output
    )

ft.app(target=main, view=ft.WEB_BROWSER)

 