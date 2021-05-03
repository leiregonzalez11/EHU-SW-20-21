package servlets;

import java.io.IOException;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import HTTPeXist.HTTPeXist;

public class NewImage extends HttpServlet{

	private static final long serialVersionUID = 1L;
	private HTTPeXist eXist;

	
	public void init(ServletConfig config) {
		System.out.println("---> Entrando en init()de listResource");
		eXist = new HTTPeXist("http://localHost:8081");
		System.out.println("---> Saliendo de init()de LoginServlet");
	}
	
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		String collection = request.getParameter("collection");
		String svg = request.getParameter("svgName");
		String resource = "<svg> Introduzca aqui su código </svg>";
		
		if (!eXist.existImage(collection,svg)) {
			
			request.setAttribute("informacion", "Error: El recurso "+ svg + " ya existe.");
			
			System.out.println("     Redireccionando a index.jsp");
			RequestDispatcher rd = request.getRequestDispatcher("/jsp/index.jsp");
			rd.forward(request, response);
		}
		
		else {
		
			eXist.subirString(collection, resource, svg);
			
			request.setAttribute("collection", collection);
			request.setAttribute("svgName", svg);
			request.setAttribute("imagenSVG", resource);
			String imagenURI = "http://localhost:8081/exist/rest/db/" + collection + "/" + svg + "/";
			request.setAttribute("imagenURI", imagenURI);
			
			System.out.println("Redireccionando a imagenEdit.jsp");
			RequestDispatcher rd = request.getRequestDispatcher("/jsp/imagenEdit.jsp");
			rd.forward(request, response);
		
		}
			
	}
	
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		
		doGet(request, response);
	}
}
