package servlets;

import java.io.IOException;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import HTTPeXist.HTTPeXist;

public class CreateCollection extends HttpServlet{
	
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
		
		if (!eXist.existCollection(collection)) {
			
			request.setAttribute("informacion", "Error: La colección "+ collection + " ya existe.");
		}
		
		else {
			
			int status = eXist.create(collection);
			
			if (status == 201) {
				request.setAttribute("informacion", "Colección "+ collection + " creada correctamente");
			} else {
				request.setAttribute("informacion", "Ha surgido un problema. Inténtelo de nuevo. (Código "+ status +")");
			}
		}
		
		
		System.out.println("     Redireccionando a index.jsp");
		RequestDispatcher rd = request.getRequestDispatcher("/jsp/index.jsp");
		rd.forward(request, response);
			
	}
	
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		
		doGet(request, response);
	}
	
	

}
