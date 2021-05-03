package servlets;

import java.io.IOException;

import javax.servlet.RequestDispatcher;
import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import HTTPeXist.HTTPeXist;

public class DeleteSvg extends HttpServlet{
	
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
		
		int status = eXist.delete(collection,svg);
		if (status == 200) {
			request.setAttribute("informacion", "Recurso "+ svg +" eliminado correctamente");
		} else {
			request.setAttribute("informacion", "Ha surgido un error. Int�ntelo de nuevo. (C�digo "+ status+")");
		}
		
		System.out.println("     Redireccionando a index.jsp");
		RequestDispatcher rd = request.getRequestDispatcher("/jsp/index.jsp");
		response.setHeader("Cache-Control", "no-cache");
		response.setDateHeader("Expires", 0);
		rd.forward(request, response);
			
	}
	
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		
		doGet(request, response);
	}

}
